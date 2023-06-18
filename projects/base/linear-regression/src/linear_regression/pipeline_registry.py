"""Project pipelines."""
from typing import Dict

from kedro.pipeline import Pipeline

import linear_regression.pipelines.model.pipeline as model_pipeline
import linear_regression.pipelines.prepare.pipeline as prepare_pipeline


def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """
    parameters = dict(n_splits=5)

    pipelines = {
        "prepare": prepare_pipeline.create_pipeline(**parameters),
        "model": model_pipeline.create_pipeline(**parameters)
    }

    pipelines["__default__"] = sum(pipelines.values())

    return pipelines
