"""
This is a boilerplate pipeline 'drop_zero_columns'
generated using Kedro 0.18.9
"""

import pandas as pd
from typing import Dict


def drop_zero_columns(dataset: pd.DataFrame, parameters: Dict) -> pd.DataFrame:
    drop_columns = []
    ratio = parameters['ratio']
    all = len(dataset)

    for column in dataset.columns:
        is_na = dataset[column].isna().sum()

        if ((all - is_na) / all) <= ratio:
            drop_columns += [column]

    return dataset.drop(drop_columns, axis=1)
