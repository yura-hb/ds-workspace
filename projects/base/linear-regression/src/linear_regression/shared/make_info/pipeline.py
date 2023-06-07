"""
This is a boilerplate pipeline 'make_info'
generated using Kedro 0.18.9
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import make_info


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(make_info,
             inputs=["dataset", "params:make_info_parameters"],
             outputs="info",
             name=kwargs.get("name"))
    ])
