"""
This is a boilerplate pipeline 'cross_validate'
generated using Kedro 0.18.9
"""

import itertools

from dataclasses import dataclass, field

from kedro.pipeline.modular_pipeline import pipeline as modular_pipeline
from kedro.pipeline import pipeline, Pipeline, node

import train_test_split.pipeline as train_test_split_module
import fold_split.pipeline as fold_split_module

from typing import Callable, List, Tuple


# TODO: Implement the estimator

@dataclass
class ModelConfiguration:
    name: str
    # A function, which should perform evaluation on the model with given sets
    # Expect the function, which accepts a list of input sets (X_train, X_valid, y_train, y_valid) and namespace
    # and outputs pipeline and the metrics dataset
    estimator: Callable[[List[str], str], Tuple[Pipeline, str]]


@dataclass
class Configuration:
    n_splits: int = 5
    train_test_split: bool = True
    models: List[ModelConfiguration] = field(default_factory=list)

    X_dataset_name: str = 'X'
    y_dataset_name: str = 'y'
    train_suffix: str = '_train'
    test_suffix: str = '_test'
    validation_suffix: str = '_validation'
    namespace: str = 'cross_validate'


def train_test_split_pipeline(config: Configuration):
    if not config.train_test_split:
        return None, config.X_dataset_name, config.y_dataset_name, "", ""

    inputs = [config.X_dataset_name, config.y_dataset_name]
    suffixes = [config.train_suffix, config.test_suffix]
    _pipeline, output_sets = train_test_split_module.create_pipeline(sets=inputs, suffixes=suffixes)

    return pipeline(
        [modular_pipeline(_pipeline, inputs=inputs, outputs=output_sets)],
        namespace='train_test_split'
    ), *output_sets


def validation_split_pipeline(config: Configuration, X_train: str, y_train: str):
    _pipeline, output_sets = fold_split_module.create_pipeline(n_splits=config.n_splits,
                                                               sets=[config.X_dataset_name, config.y_dataset_name],
                                                               suffixes=[config.train_suffix, config.validation_suffix])

    return pipeline(
        modular_pipeline(_pipeline, inputs={"X": X_train, "y": y_train}),
        namespace="fold_split"
    ), output_sets


def evaluate_model_configuration_pipeline(config: Configuration, sets: List[str]):
    pipelines = []
    metrics = []

    numbers_of_sets = 4
    sliced = itertools.islice(sets, numbers_of_sets)

    for index, pair in enumerate(sliced):

        for model_config in config.models:
            namespace = f'estimate_{index}'
            estimate_pipeline, metrics_dataset = model_config.estimator(pair, namespace)

            pipelines += estimate_pipeline
            metrics += metrics_dataset

    return pipeline(
        pipelines,
        namespace="estimation"
    ), metrics


def __append__(pipelines, _pipeline, *args):
    if _pipeline is None:
        return pipelines, *args

    return pipelines + [_pipeline], *args


def create_pipeline(config: Configuration = Configuration()) -> Pipeline:
    pipelines = []
    pipelines, X_train, y_train, X_test, y_test = __append__(pipelines, *train_test_split_pipeline(config))
    pipelines, output_sets = __append__(pipelines, *validation_split_pipeline(config, X_train, y_train))
    pipelines, metrics = __append__(pipelines, *evaluate_model_configuration_pipeline(config, output_sets))

    return pipeline(
        pipelines,
        namespace=config.namespace
    )
