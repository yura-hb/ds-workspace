
import logging
from typing import Tuple, Dict

import optuna


from .base_optimizer import BaseOptimizer
from ..load_class import load_class, load_constructor

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class OptunaOptimizer(BaseOptimizer):

    def __init__(self, parameters, configuration):
        super().__init__(parameters, configuration)

        self.study = None

    def optimize(self, X_train, X_test, y_train, y_test):
        study, optimize_parameters = self.__make_study__()

        self.study = study

        def objective(trial):
            parameters = self.__make_parameters__(trial)
            model = self.make_model(parameters)

            return model.ordered_metrics

        study.optimize(objective, **optimize_parameters)

    def __make_study__(self) -> Tuple[optuna.Study, Dict]:
        optuna.logging.enable_propagation()
        optuna.logging.disable_default_handler()

        optuna_parameters = self.parameters['optuna_parameters']

        study = optuna.create_study(
            storage=optuna_parameters.get('storage'),
            sampler=self.__make_sampler__(optuna_parameters),
            pruner=self.__make_pruner__(optuna_parameters),
            study_name=optuna_parameters.get('study_name'),
            load_if_exists=optuna_parameters.get('load_if_exists'),
            direction=optuna_parameters.get('direction'),
            directions=optuna_parameters.get('directions')
        )

        # TODO: - Implement better postprocessing
        study.set_metric_names(self.parameters['metrics'].keys())

        optimize_params = dict(n_jobs=self.parameters.get('n_jobs') or 1,
                               n_trials=self.parameters.get('n_trials'),
                               gc_after_trial=self.parameters.get('gc_after_trial') or True,
                               show_progress_bar=self.parameters.get('show_progress_bar') or False)

        return study, optimize_params

    def __make_pruner__(self, parameters) -> optuna.pruners.BasePruner:
        return self.__make_optuna_object__(
            optuna.pruners,
            'BasePruner',
            'pruner',
            self.configuration.pruner,
            self.configuration.pruner_parameters,
            parameters
        )

    def __make_sampler__(self, parameters) -> optuna.samplers.BaseSampler:
        return self.__make_optuna_object__(
            optuna.samplers,
            'BaseSampler',
            'sampler',
            self.configuration.sampler,
            self.configuration.sampler_parameters,
            parameters
        )

    def __make_optuna_object__(self, module, base_class_key, key, custom_value, custom_args, configuration):
        if key not in configuration:
            return None

        cls = configuration[key]['class']

        if cls == 'custom':
            return custom_value

        object_class = load_class(module, cls)

        parameters = configuration['parameters']

        for key, value in custom_args:
            # A custom merge of two dictionaries to propagate custom parameters for nested object
            if key in parameters.keys() and isinstance(value, dict):
                parameters[key] |= value
                continue

            parameters[key] = value

        # In some cases, optuna object will be a wrapper around actual item. In parameters, we expect, that such object
        # will have nested specification.
        signature = load_constructor(object_class)

        for key, parameter in signature.parameters:
            if base_class_key in parameter.annotation and key in parameters and parameters[key] is dict:
                parameters[key] = self.__make_optuna_object__(
                    module, base_class_key, key, None, None, parameters[key]
                )

        return object_class(**parameters)

    def __make_parameters__(self, trial: optuna.Trial) -> Dict:
        model_parameters = self.parameters['model']

        return self.__fill_parameters__(trial, model_parameters, is_root=True)

    def __fill_parameters__(self, trial: optuna.Trial, parameters: Dict, is_root: bool = False, namespace: str = '') -> Dict:
        result = parameters

        if is_root and result['class'] == 'multi-model':
            result['parameters']['class'] = self.__suggest_parameter__(trial, result['parameters']['class'], 'class')
            # Filter out other model configurations
            result['parameters']['parameters'] = result['parameters']['parameters'][result['parameters']['class']]

        for key, value in result.items():
            is_value_dict = isinstance(value, Dict)

            if not is_value_dict:
                continue

            name = namespace + '.' + key

            if 'optimize' in value:
                result[key] = self.__suggest_parameter__(trial, value, name=name)
                continue

            result[key] = self.__fill_parameters__(trial, value, namespace=name)

        return result

    @staticmethod
    def __suggest_parameter__(trial: optuna.Trial, value, name):
        parameters = value.get('parameters') or []

        match value['type']:
            case 'float':
                return trial.suggest_float(name=name, **parameters)
            case 'categorical':
                return trial.suggest_categorical(name=name, **parameters)
            case 'int':
                return trial.suggest_int(name=name, **parameters)
            case 'discrete_uniform':
                return trial.suggest_discrete_uniform(name=name, **parameters)
            case 'log_uniform':
                return trial.suggest_loguniform(name=name, **parameters)
            case 'uniform':
                return trial.suggest_uniform(name=name, **parameters)
