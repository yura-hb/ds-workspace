"""
This is a boilerplate pipeline 'prepare'
generated using Kedro 0.18.8
"""

from kedro.pipeline.modular_pipeline import pipeline as modular_pipeline
from kedro.pipeline import pipeline, Pipeline, node

from .nodes import process

import linear_regression.shared.make_info.pipeline as make_info_pipeline
import linear_regression.shared.take_columns.pipeline as take_columns_pipeline
import linear_regression.shared.train_test_split.pipeline as train_test_split_pipeline
import linear_regression.shared.fold_split.pipeline as fold_split_pipeline
import linear_regression.shared.drop_zero_columns.pipeline as drop_zero_columns
import linear_regression.shared.drop_columns.pipeline as drop_columns
import linear_regression.shared.one_hot_encode.pipeline as one_hot_encode
import linear_regression.shared.date_to_float.pipeline as date_to_float
import linear_regression.shared.plot_corr_matrix.pipeline as plot_corr_matrix
import linear_regression.shared.fill_na.pipeline as fill_na
import linear_regression.shared.drop_constant_columns.pipeline as drop_constant_columns


def make_preprocess_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        # X preprocessing
        modular_pipeline(take_columns_pipeline.create_pipeline(),
                         parameters={"params:take_column_parameters": "params:take_X_parameters"},
                         outputs={"filtered_dataset": "X_orig"}),
        node(process,
             inputs=['X_orig'],
             outputs='X_encoded_0'),
        # modular_pipeline(one_hot_encode.create_pipeline(),
        #                  inputs={"dataset": "X_encoded_0"},
        #                  outputs={"dataset_out": "X_encoded_1"}),
        modular_pipeline(date_to_float.create_pipeline(),
                         inputs={"dataset": "X_encoded_0"},
                         outputs={"dataset_out": "X_encoded_2"}),
        modular_pipeline(drop_zero_columns.create_pipeline(),
                         inputs={"dataset": "X_encoded_2"},
                         outputs={"dataset_out": "X_encoded_3"}),
        modular_pipeline(drop_columns.create_pipeline(),
                         inputs={"dataset": "X_encoded_3"},
                         outputs={"dataset_out": "X_encoded_4"}),
        modular_pipeline(fill_na.create_pipeline(),
                         inputs={"dataset": "X_encoded_4"},
                         outputs={"dataset_out": "X_encoded_5"}),
        modular_pipeline(drop_constant_columns.create_pipeline(),
                         inputs={"dataset": "X_encoded_5"},
                         outputs={"dataset_out": "X"}),
        # y preprocessing
        modular_pipeline(take_columns_pipeline.create_pipeline(),
                         inputs="dataset",
                         parameters={"params:take_column_parameters": "params:take_y_parameters"},
                         outputs={"filtered_dataset": "y"},
                         namespace="take_y"),
        # Post-info
        modular_pipeline(plot_corr_matrix.create_pipeline(),
                         inputs={"dataset": "X"},
                         outputs={"figure": "X_corr_matrix_fig"}),

    ], inputs=['dataset'],
       outputs=['X', 'y'],
       namespace="data_preprocess")


def split_pipeline(**kwargs) -> Pipeline:
    split_pipeline, output_sets = fold_split_pipeline.create_pipeline(folds=5, return_output_sets=True)

    return pipeline([
        modular_pipeline(train_test_split_pipeline.create_pipeline(sets=["X", "y"])),
        modular_pipeline(split_pipeline, inputs={"X": "X_train", "y": "y_train"})
    ], inputs=['X', 'y'],
       outputs=['X_test', 'y_test', *output_sets],
       namespace="split")


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        modular_pipeline(make_info_pipeline.create_pipeline(),
                         outputs={"info": "all_columns_info"}),
        make_preprocess_pipeline(),
        split_pipeline()
    ])
