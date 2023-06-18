
from abc import ABC, abstractmethod
from typing import Dict

from ..models import BaseModel
from ..models import SKLearnModel


class BaseOptimizer(ABC):

    def __init__(self, parameters, configuration):
        self.parameters = parameters
        self.configuration = configuration

    @abstractmethod
    def optimize(self, X_train, X_test, y_train, y_test):
        pass

    @property
    @abstractmethod
    def result(self):
        pass

    def make_model(self, parameters: Dict) -> BaseModel:
        cls = parameters['class']
        components = cls.split('.')
        prefix, model_name = components[0], '.'.join(components[1:])

        model_parameters = parameters['parameters']
        args = (model_parameters, self.parameters['metrics'], self.configuration)

        match prefix:
            case 'multi-model':
                cls = model_parameters['class']

                new_parameters = {
                    'class': cls,
                    'parameters': model_parameters['parameters'][cls]
                }

                return self.make_model(new_parameters)
            case 'sklearn':
                return SKLearnModel(cls, *args)
            case 'custom':
                return self.configuration.model[model_name](model_parameters, *args)
            case '_':
                pass
