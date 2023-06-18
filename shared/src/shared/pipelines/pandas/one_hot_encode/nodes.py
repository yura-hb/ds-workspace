"""
This is a boilerplate pipeline 'one_hot_encode'
generated using Kedro 0.18.9
"""

import pandas as pd
from typing import Dict


def one_hot_encode(dataset: pd.DataFrame, parameters: Dict) -> pd.DataFrame:
    preserve_columns = parameters.get('preserve_columns') or False

    df = pd.DataFrame()

    if preserve_columns:
        del parameters['preserve_columns']

        df = dataset[parameters['columns']]

    dataset = pd.get_dummies(dataset, **parameters)

    return dataset.join(df) if len(df) > 0 else dataset
