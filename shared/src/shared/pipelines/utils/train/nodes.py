"""
This is a boilerplate pipeline 'train'
generated using Kedro 0.18.9
"""

from utils.optimizers import make_optimizer


def train(X_train, X_test, y_train, y_test, parameters, configuration):
    optimizer = make_optimizer(parameters, configuration)
    optimizer.optimize(X_train, X_test, y_train, y_test)

    return ...