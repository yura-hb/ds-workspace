"""
This is a boilerplate pipeline 'prepare'
generated using Kedro 0.18.8
"""

from kedro.pipeline.modular_pipeline import pipeline as modular_pipeline
from kedro.pipeline import pipeline, Pipeline

import linear_regression.shared.make_info.pipeline as make_info_pipeline
import linear_regression.shared.take_columns.pipeline as take_columns_pipeline
import linear_regression.shared.train_test_split.pipeline as train_test_split_pipeline
import linear_regression.shared.fold_split.pipeline as fold_split_pipeline


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        modular_pipeline(make_info_pipeline.create_pipeline(),
                         outputs={"info": "all_columns_info"}),
        modular_pipeline(take_columns_pipeline.create_pipeline(),
                         inputs="dataset",
                         parameters={"params:take_column_parameters": "params:take_X_parameters"},
                         outputs={"filtered_dataset": "X"},
                         namespace="take_X"),
        modular_pipeline(take_columns_pipeline.create_pipeline(),
                         inputs="dataset",
                         parameters={"params:take_column_parameters": "params:take_y_parameters"},
                         outputs={"filtered_dataset": "y"},
                         namespace="take_y"),
        modular_pipeline(train_test_split_pipeline.create_pipeline(sets=["X", "y"]),
                         namespace=""),
        modular_pipeline(fold_split_pipeline.create_pipeline(folds=5),
                         inputs={"X": "X_train", "y": "y_train"},
                         namespace="")
    ])
