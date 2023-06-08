"""
This is a boilerplate pipeline 'drop_constant_columns'
generated using Kedro 0.18.9
"""

import pandas as pd


def drop_constant_columns(dataset: pd.DataFrame) -> pd.DataFrame:
    return dataset.loc[:, (dataset != dataset.iloc[0]).any()]