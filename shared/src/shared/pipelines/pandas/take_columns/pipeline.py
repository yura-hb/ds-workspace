"""
This is a boilerplate pipeline 'take_columns'
generated using Kedro 0.18.9
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import take_columns


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            take_columns,
            inputs=["dataset", "params:take_column_parameters"],
            outputs="filtered_dataset",
            name=kwargs.get("name")
        )
    ])
