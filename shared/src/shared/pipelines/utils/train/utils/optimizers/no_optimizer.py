

from .base_optimizer import BaseOptimizer


class NoOptimizer(BaseOptimizer):

    def optimize(self, X_train, X_test, y_train, y_test):
        model = self.make_model(parameters=self.parameters['parameters'])
        model.train(X_train, X_test, y_train, y_test)

