from typing import Dict, List

from .base_model import BaseModel
from ..reflection_utils import load_nested_class


class SKLearnModel(BaseModel):

    def __init__(self, model_name, parameters, metrics, configuration):
        super().__init__(parameters, metrics, configuration)

        self.model_name = model_name
        self.model = load_nested_class(model_name)(**parameters)

    def train(self, X_train, X_test, y_train, y_test):
        self.model = self.model.fit(X_train, y_train)

        y_pred = self.model.predict(X_test if self.configuration.validate else X_train)
        y_true = y_test if self.configuration.validate else y_train

        self.evaluated_metrics = self.__evaluate_metrics__(
            y_pred, y_true, configuration=self.configuration, metrics=self.metrics_ids
        )

    @property
    def base_model(self):
        return self.model

    @property
    def metrics(self) -> Dict:
        return self.evaluated_metrics

    @property
    def ordered_metrics(self) -> List:
        return tuple(self.evaluated_metrics.values())
