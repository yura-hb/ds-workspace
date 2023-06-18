
from .base_optimizer import BaseOptimizer
from .no_optimizer import NoOptimizer
from .optuna_optimizer import OptunaOptimizer


def make_optimizer(parameters, configuration) -> BaseOptimizer:
    if 'optuna_parameters' in parameters:
        return OptunaOptimizer(parameters, configuration)

    return NoOptimizer(parameters, configuration)
