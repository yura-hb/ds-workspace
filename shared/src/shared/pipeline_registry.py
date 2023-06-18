"""Project pipelines."""

import os
import importlib
import importlib_resources
import warnings
import traceback

from typing import Dict

from kedro.framework.project import find_pipelines, PACKAGE_NAME, IMPORT_ERROR_MESSAGE, _create_pipeline
from kedro.pipeline import Pipeline, pipeline


def find_pipelines_recursively() -> dict[str, Pipeline]:
    """Automatically find modular pipelines having a ``create_pipeline``
    function. By default, projects created using Kedro 0.18.3 and higher
    call this function to autoregister pipelines upon creation/addition.

    For more information on the pipeline registry and autodiscovery, see
    https://kedro.readthedocs.io/en/latest/nodes_and_pipelines/pipeline_registry.html

    Returns:
        A generated mapping from pipeline names to ``Pipeline`` objects.

    Warns:
        UserWarning: When a module does not expose a ``create_pipeline``
            function, the ``create_pipeline`` function does not return a
            ``Pipeline`` object, or if the module import fails up front.
    """
    pipeline_obj = None

    # Handle the simplified project structure found in several starters.
    pipeline_module_name = f"{PACKAGE_NAME}.pipeline"
    try:
        pipeline_module = importlib.import_module(pipeline_module_name)
    except Exception as exc:  # pylint: disable=broad-except
        if str(exc) != f"No module named '{pipeline_module_name}'":
            warnings.warn(
                IMPORT_ERROR_MESSAGE.format(
                    module=pipeline_module_name, tb_exc=traceback.format_exc()
                )
            )
    else:
        pipeline_obj = _create_pipeline(pipeline_module)

    pipelines_dict = {"__default__": pipeline_obj or pipeline([])}
    pipelines_dict |= find_pipelines(None)

    return pipelines_dict


def find_pipelines(directory):
    try:
        path = f"{PACKAGE_NAME}.pipelines" if directory is None else f"{PACKAGE_NAME}.pipelines.{directory}"
        pipelines_package = importlib_resources.files(path)
    except ModuleNotFoundError as exc:
        print(exc)
        return {}

    pipelines_dict = {}

    for pipeline_dir in pipelines_package.iterdir():
        if not pipeline_dir.is_dir():
            continue

        pipeline_name = pipeline_dir.name

        if pipeline_name == "__pycache__":
            continue

        pipeline_module_name = f"{PACKAGE_NAME}.pipelines"

        if directory is not None:
            pipeline_module_name += f".{directory}"

        pipeline_module_name += f".{pipeline_name}"

        try:
            pipeline_module = importlib.import_module(pipeline_module_name)
        except:  # pylint: disable=bare-except  # noqa: E722
            warnings.warn(
                IMPORT_ERROR_MESSAGE.format(
                    module=pipeline_module_name, tb_exc=traceback.format_exc()
                )
            )
            continue

        if not hasattr(pipeline_module, "create_pipeline"):
            dir_path = ""
            path = pipeline_dir

            while True:
                path, tail = os.path.split(path)

                if tail == 'pipelines':
                    break

                dir_path = tail + "." + dir_path

            dir_path = dir_path.strip('.')

            pipelines_dict |= find_pipelines(dir_path)
        else:
            pipeline_obj = _create_pipeline(pipeline_module)

            if pipeline_obj is not None:
                pipelines_dict[pipeline_name] = pipeline_obj

    return pipelines_dict


def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """
    pipelines = find_pipelines_recursively()
    pipelines["__default__"] = sum(pipelines.values())
    return pipelines
