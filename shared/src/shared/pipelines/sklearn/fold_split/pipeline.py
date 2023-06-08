"""
This is a boilerplate pipeline 'fold_split'
generated using Kedro 0.18.9
"""

import functools

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import split
from typing import Union, Tuple, List


def create_pipeline(**kwargs) -> Union[Pipeline | Tuple[Pipeline, List]]:
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

    out_pipeline = pipeline([
        node(
            _split,
            inputs=[*sets, "params:fold_split_parameters"],
            outputs=output_sets,
            name=kwargs.get("name")
        )
    ])

    return_output_sets = kwargs.get("return_output_sets") or False

    if return_output_sets:
        return out_pipeline, output_sets
    else:
        return out_pipeline
