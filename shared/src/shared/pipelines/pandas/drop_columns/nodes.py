"""
This is a boilerplate pipeline 'drop_columns'
generated using Kedro 0.18.9
"""

import pandas as pd


def drop_columns(dataset: pd.DataFrame, parameters) -> pd.DataFrame:
    columns = parameters["columns"]
    columns = set(columns).intersection(dataset.columns)

    return dataset.drop(columns, axis=1)
