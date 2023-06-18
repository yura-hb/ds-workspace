

from .base_optimizer import BaseOptimizer


class NoOptimizer(BaseOptimizer):

    def __init__(self, parameters, configuration):
        super().__init__(parameters, configuration)
        self.model = None

    def optimize(self, X_train, X_test, y_train, y_test):
        self.model = self.make_model(parameters=self.parameters['model']['parameters'])
        self.model.train(X_train, X_test, y_train, y_test)

    @property
    def result(self):
        return [self.model.base_model], [self.parameters['model']['parameters']], [self.model.metrics]
