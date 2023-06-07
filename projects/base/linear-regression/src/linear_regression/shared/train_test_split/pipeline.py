"""
This is a boilerplate pipeline 'train_test_split'
generated using Kedro 0.18.9
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import split


def create_pipeline(**kwargs) -> Pipeline:
    assert "sets" in kwargs, "Expect 'sets' parameter specifying input datasets"

    sets = kwargs["sets"]
    output_sets = []

    for dataset in sets:
        output_sets += [f"{dataset}_train", f"{dataset}_test"]

    return pipeline([
        node(
            split,
            inputs=[*sets, "params:train_test_split_parameters"],
            outputs=output_sets,
            name=kwargs.get("name")
        )
    ])
