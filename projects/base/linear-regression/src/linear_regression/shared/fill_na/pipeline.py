"""
This is a boilerplate pipeline 'fill_na'
generated using Kedro 0.18.9
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import fillna


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(fillna,
             inputs=["dataset", "params:fill_na_parameters"],
             outputs="dataset_out",
             name=kwargs.get("name"))
    ])

