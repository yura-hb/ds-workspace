"""
This is a boilerplate pipeline 'one_hot_encode'
generated using Kedro 0.18.9
"""

import pandas as pd
from typing import Dict


def one_hot_encode(dataset: pd.DataFrame, parameters: Dict) -> pd.DataFrame:
    return pd.get_dummies(dataset, **parameters)
