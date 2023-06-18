"""
This is a boilerplate pipeline 'fold_split'
generated using Kedro 0.18.9
"""

import functools

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import split
from typing import Union, Tuple, List


def create_pipeline(
   n_splits: int,
   sets: List[str] = None,
   suffixes: List[str] = None,
   return_output_sets: bool = True, **kwargs
) -> Union[Pipeline | Tuple[Pipeline, List]]:
    if sets is None:
        sets = ['X', 'y']

    if suffixes is None:
        suffixes = ['X', 'y']

    assert len(sets) == 2, "Expect, that sets parameter is of length 2"
    assert len(suffixes) == 2, "Expect, that suffixes parameter is of length 2"

    output_sets = []

    for i in range(n_splits):
        for dataset in sets:
            output_sets += [f"{dataset}_{suffix}_{i}" for suffix in suffixes]

    _split = functools.partial(split, n_folds=n_splits)
    _split = functools.update_wrapper(_split, split)

    out_pipeline = pipeline([
        node(
            _split,
            inputs=[*sets, "params:fold_split_parameters"],
            outputs=output_sets,
            name=kwargs.get("name")
        )
    ])

    if return_output_sets:
        return out_pipeline, output_sets
    else:
        return out_pipeline
