"""
This is a boilerplate pipeline 'model'
generated using Kedro 0.18.9
"""

import numpy as np

from kedro.pipeline.modular_pipeline import pipeline as modular_pipeline
from kedro.pipeline import pipeline, Pipeline, node

import linear_regression.shared.train.pipeline as train_pipeline


def average_distance_metric(y_true, y_pred, squared: bool = False):
    y_true = y_true.to_numpy().reshape(-1)
    mean = float(np.mean(y_true - y_pred))

    return np.sqrt(mean) if squared else mean


def train_on_split_pipeline(split: int = 0) -> Pipeline:
    X_train_key, y_train_key = f"X_train_{split}", f"y_train_{split}"
    X_valid_key, y_valid_key = f"X_valid_{split}", f"y_valid_{split}"

    inputs_map = {"X_train": X_train_key, "X_test": X_valid_key, "y_train": y_train_key, "y_test": y_valid_key}

    optuna_cnf = train_pipeline.OptunaConfiguration

    configuration = train_pipeline.Configuration(
        metrics={
            'average_distance': average_distance_metric
        },
        optuna_configuration=train_pipeline.OptunaConfiguration(
            study_name=f"split_{split}",
            result=optuna_cnf.Result(kind=optuna_cnf.Result.Kind.top_k_per_class_models, value=5)
        )
    )

    return pipeline([
        modular_pipeline(train_pipeline.create_pipeline(configuration), inputs=inputs_map)
    ], inputs=[X_train_key, X_valid_key, y_train_key, y_valid_key],
       outputs=[],
       namespace=f"train_split_{split}")


def create_pipeline(**kwargs) -> Pipeline:
    n_splits = kwargs['n_splits']

    return pipeline([
        train_on_split_pipeline(split=i) for i in range(n_splits)
    ])
