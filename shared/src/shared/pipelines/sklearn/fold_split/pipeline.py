"""
This is a boilerplate pipeline 'fold_split'
generated using Kedro 0.18.9
"""

import functools

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import split


def create_pipeline(**kwargs) -> Pipeline:
    assert "folds" in kwargs, "Expect 'folds' parameter specifying the number of splits"

    sets = kwargs.get("sets") or ["X", "y"]
    folds = kwargs["folds"]
    output_sets = []

    assert len(sets) == 2, "Expect, that sets parameter is of length 2"

    for i in range(folds):
        for dataset in sets:
            output_sets += [f"{dataset}_train_{i}", f"{dataset}_val_{i}"]

    _split = functools.partial(split, n_folds=folds)
    _split = functools.update_wrapper(_split, split)

    return pipeline([
        node(
            _split,
            inputs=[*sets, "params:fold_split_parameters"],
            outputs=output_sets,
            name=kwargs.get("name")
        )
    ])
