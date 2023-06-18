
import logging
from typing import Tuple, Dict

import optuna
import copy

from .base_optimizer import BaseOptimizer
from ..reflection_utils import load_obj, load_constructor


log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


multi_model_key = 'multi-model'


class OptunaOptimizer(BaseOptimizer):

    def __init__(self, parameters, configuration):
        super().__init__(parameters, configuration)

        self.study = None
        self.optimization_result = None

    def optimize(self, X_train, X_test, y_train, y_test):
        study, optimize_parameters = self.__make_study__()
        datasets = (X_train, X_test, y_train, y_test)

        self.study = study

        def objective(trial):
            model = self.__train_model__(datasets, trial)

            return model.ordered_metrics

        study.optimize(objective, **optimize_parameters)

        self.optimization_result = self.__make_optimization_result__(datasets, study)

    @property
    def result(self):
        return self.optimization_result

    def __make_study__(self) -> Tuple[optuna.Study, Dict]:
        optuna.logging.enable_propagation()
        optuna.logging.disable_default_handler()

        optuna_parameters = self.parameters['optuna_parameters']

        study = optuna.create_study(
            storage=optuna_parameters.get('storage'),
            sampler=self.__make_sampler__(optuna_parameters),
            pruner=self.__make_pruner__(optuna_parameters),
            study_name=self.configuration.optuna_configuration.study_name or optuna_parameters.get('study_name'),
            load_if_exists=optuna_parameters.get('load_if_exists'),
            direction=optuna_parameters.get('direction'),
            directions=optuna_parameters.get('directions')
        )

        study.set_metric_names(optuna_parameters['metric_names'])

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
            self.configuration.optuna_configuration.pruner,
            self.configuration.optuna_configuration.pruner_parameters,
            parameters
        )

    def __make_sampler__(self, parameters) -> optuna.samplers.BaseSampler:
        return self.__make_optuna_object__(
            optuna.samplers,
            'BaseSampler',
            'sampler',
            self.configuration.optuna_configuration.sampler,
            self.configuration.optuna_configuration.sampler_parameters,
            parameters
        )

    def __make_optuna_object__(self, module, base_class_key, key, custom_value, custom_args, configuration):
        if key not in configuration:
            return None

        cls = configuration[key]['class']

        if cls == 'custom':
            return custom_value

        object_class = load_obj(module, cls)

        parameters = configuration[key]['parameters']

        for key, value in custom_args:
            # A custom merge of two dictionaries to propagate custom parameters for nested object
            if key in parameters.keys() and isinstance(value, dict):
                parameters[key] |= value
                continue

            parameters[key] = value

        # In some cases, optuna object will be a wrapper around actual item. In parameters, we expect, that such object
        # will have nested specification.
        signature = load_constructor(object_class)

        for key, parameter in signature.parameters.items():
            # Skip parameter without annotation (For optuna it is self)
            if parameter.annotation == parameter.empty:
                continue

            # TODO: - Improve the solution with type search
            if base_class_key in str(parameter.annotation) and key in parameters and parameters[key] is dict:
                parameters[key] = self.__make_optuna_object__(
                    module, base_class_key, key, None, None, parameters[key]
                )

        return object_class(**parameters)

    def __make_optimization_result__(self, datasets, study):
        result_info = self.configuration.optuna_configuration.result
        kind = result_info.kind

        trials = []

        match kind:
            case kind.best_model:
                trials = [study.best_trials[0]]
            case kind.best_per_class_models:
                assert self.parameters['model']['class'] == multi_model_key

                returned_trials = set()

                def filter_key(trial):
                    nonlocal returned_trials

                    key = trial.params['class']
                    is_returned = key in returned_trials
                    returned_trials.add(key)

                    return is_returned

                trials = sorted(study.trials, key=lambda x: x.values)
                trials = filter(filter_key, trials)
            case kind.top_k_models:
                suffix = min(len(study.trials), result_info.value)
                trials = sorted(study.trials, key=lambda x: x.values)[:suffix]
            case kind.top_k_per_class_models:
                assert self.parameters['model']['class'] == multi_model_key

                max_trials = result_info.value
                returned_trials = dict()

                def filter_key(trial):
                    nonlocal returned_trials

                    key = trial.params['class']
                    returned_trials[key] = (returned_trials.get(key) or 0) + 1

                    return returned_trials[key] < max_trials

                trials = sorted(study.trials, key=lambda x: x.values)
                trials = filter(filter_key, trials)
            case _:
                raise ValueError(f'Unknown kind for result {result_info.value}')

        models = [self.__train_model__(datasets, trial) for trial in trials]
        parameters = [trial.params for trial in trials]
        metrics = [trial.values for trial in trials]

        return models, parameters, metrics

    def __train_model__(self, datasets, trial):
        parameters = self.__make_parameters__(trial)
        model = self.make_model(parameters)

        model.train(*datasets)

        return model

    def __make_parameters__(self, trial: optuna.Trial) -> Dict:
        model_parameters = copy.deepcopy(self.parameters['model'])

        return self.__fill_parameters__(trial, model_parameters, is_root=True)

    def __fill_parameters__(self, trial: optuna.Trial, parameters: Dict, is_root: bool = False, namespace: str = '') -> Dict:
        result = parameters

        if is_root and result['class'] == multi_model_key:
            new_parameters = dict()

            new_parameters['class'] = self.__suggest_parameter__(trial, result['parameters']['class'], 'class')
            # Filter out other model configurations
            new_parameters['parameters'] = result['parameters']['parameters'][new_parameters['class']]

            result = new_parameters

        for key, value in result.items():
            is_value_dict = isinstance(value, Dict)

            if not is_value_dict:
                continue

            name = '' if is_root else (namespace + ('.' if len(namespace) > 0 else '') + key)

            if 'optimize' in value:
                result[key] = self.__suggest_parameter__(trial, value, name=name)
                continue

            result[key] = self.__fill_parameters__(trial, value, namespace=name)

        return result

    @staticmethod
    def __suggest_parameter__(trial: optuna.Trial, value, name):
        parameters = value.get('parameters') or dict()

        match value['type']:
            case 'float':
                return trial.suggest_float(name=name, **parameters)
            case 'categorical':
                return trial.suggest_categorical(name=name, **parameters)
            case 'bool':
                return trial.suggest_categorical(name=name, choices=[True, False])
            case 'int':
                return trial.suggest_int(name=name, **parameters)
            case 'discrete_uniform':
                return trial.suggest_discrete_uniform(name=name, **parameters)
            case 'log_uniform':
                return trial.suggest_loguniform(name=name, **parameters)
            case 'uniform':
                return trial.suggest_uniform(name=name, **parameters)
            case _:
                raise ValueError(f"Unknown type '{value['type']}' presented for name { name }")
