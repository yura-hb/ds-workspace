"""
This is a boilerplate pipeline 'drop_constant_columns'
generated using Kedro 0.18.9
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import drop_constant_columns


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(drop_constant_columns,
             inputs=["dataset"],
             outputs="dataset_out",
             name=kwargs.get("name"))
    ])

