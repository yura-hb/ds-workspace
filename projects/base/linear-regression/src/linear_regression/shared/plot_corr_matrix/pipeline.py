"""
This is a boilerplate pipeline 'plot_corr_matrix'
generated using Kedro 0.18.9
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import plot_corr_matrix


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(plot_corr_matrix,
             inputs=["dataset", "params:plot_corr_matrix_parameters"],
             outputs="figure",
             name=kwargs.get("name"))
    ])

