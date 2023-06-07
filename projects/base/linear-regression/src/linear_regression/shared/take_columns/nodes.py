"""
This is a boilerplate pipeline 'take_columns'
generated using Kedro 0.18.9
"""

import pandas as pd
from typing import Dict


def take_columns(df: pd.DataFrame, parameters: Dict) -> pd.DataFrame:
    columns = parameters["columns"]
    exclude = parameters["exclude"]
    columns = set(df.columns).difference(columns) if exclude else set(df.columns).intersection(columns)

    return df.loc[:, columns]
