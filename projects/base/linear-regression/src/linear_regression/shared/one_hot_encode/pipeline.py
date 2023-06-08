"""
This is a boilerplate pipeline 'one_hot_encode'
generated using Kedro 0.18.9
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import one_hot_encode


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(one_hot_encode,
             inputs=["dataset", "params:one_hot_encode_parameters"],
             outputs="dataset_out",
             name=kwargs.get("name"))
    ])

