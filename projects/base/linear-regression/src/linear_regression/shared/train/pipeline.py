"""
This is a boilerplate pipeline 'train'
generated using Kedro 0.18.9
"""

import functools
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Callable, Any, Dict, Union
from numbers import Real

import optuna
from kedro.pipeline import Pipeline, pipeline, node

from .nodes import train

# TODO: - Implement optuna optimization for custom model with its own metric
# TODO: - Implement custom parameters such as sample weight

# TODO: - Visualization:
#   1. Weights distribution
#   2.

@dataclass
class OptunaConfiguration:
    # Optuna study name
    study_name: str = None
    # Optuna sampler. The sampler will be used only `custom` value is specified for `class` key in the parameters
    sampler: optuna.samplers.BaseSampler = None
    # Custom parameters used for sampler construction. You can specify here methods and values,
    # which can be used for sampler construction
    # Note, it is discarded, if sampler is not None.
    sampler_parameters: Dict[str, Callable] = field(default_factory=dict)
    # Optuna pruner. The pruner will be used only `custom` value is specified for `class` key in the parameters
    pruner: optuna.pruners.BasePruner = None
    # Custom parameters used for pruner construction. You can specify here methods and values,
    # which can be used for pruner construction.
    # Note, it is discarded, if pruner is not None.
    pruner_parameters: Dict[str, Callable] = field(default_factory=dict)


@dataclass
class Configuration:
    # If True, then `X_test`, `y_test` values will be used for evaluation. Otherwise, `X_train` and `y_train` will be
    # used.
    validate: bool = True
    # A dict of custom models to use. The key must correspond to the key in pipeline parameters. For instance, if
    # in parameters there is a `custom.abc.some_model`, then the model key must be `abc.some_model`
    model: Dict[str, Any] = None
    # A dict of custom metrics to use. The key must correspond to the key in pipeline parameters. For instance, if
    # in parameters there is a `custom.some.metric`, then the model key must be `some.metric`.
    # The metric is a function, which accepts `y_true`, `y_pred` as parameters and can return either named dictionary
    # or a single value
    metrics: Dict[str, Callable[[Any, Any], Union[OrderedDict | Real]]] = None
    # Configuration of optuna
    optuna_configuration: OptunaConfiguration = field(default_factory=OptunaConfiguration)


def create_pipeline(configuration, **kwargs) -> Pipeline:
    __train__ = functools.partial(train, configuration=configuration)

    if not configuration.validate:
        __train__ = functools.partial(__train__, X_test=None, y_test=None)

    __train__ = functools.update_wrapper(__train__, train)

    inputs = ['X_train', 'X_test', 'y_train', 'y_test'] if configuration.validate else ['X_train', 'y_train']
    inputs += ['params:train_parameters']

    return pipeline([
        node(
            __train__,
            inputs=inputs,
            outputs=["model", "params", "metrics"],
            name=kwargs.get("name")
        )
    ])
