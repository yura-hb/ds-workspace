

import sklearn

from .base_model import BaseModel
from typing import Dict, List

from ..load_class import load_class


class SKLearnModel(BaseModel):

    def __init__(self, model_name, parameters, configuration):
        super().__init__(parameters, configuration)

        self.model_name = model_name
        self.model = load_class(sklearn, model_name)(*parameters)

    def train(self, X_train, X_test, y_train, y_test):


        pass


    def evaluate(self):
        pass

    @property
    def metrics(self) -> Dict:
        pass

    @property
    def ordered_metrics(self) -> List:
        pass