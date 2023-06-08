"""
This is a boilerplate pipeline 'date_to_float'
generated using Kedro 0.18.9
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import convert_date_to_float


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(convert_date_to_float,
             inputs=["dataset", "params:date_to_float_parameters"],
             outputs="dataset_out",
             name=kwargs.get("name"))
    ])
