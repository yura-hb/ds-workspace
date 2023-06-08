"""
This is a boilerplate pipeline 'drop_zero_columns'
generated using Kedro 0.18.9
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import drop_zero_columns


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(drop_zero_columns,
             inputs=["dataset", "params:drop_zero_columns_parameters"],
             outputs="dataset_out",
             name=kwargs.get("name"))
    ])
