

from abc import ABC, abstractmethod

from typing import Dict, Tuple


class BaseModel(ABC):

    def __init__(self, parameters, configuration):
        self.parameters = parameters
        self.configuration = configuration

    @abstractmethod
    def train(self, X_train, X_test, y_train, y_test):
        pass

    @abstractmethod
    @property
    def metrics(self) -> Dict:
        pass

    @abstractmethod
    @property
    def ordered_metrics(self) -> Tuple:
        pass

