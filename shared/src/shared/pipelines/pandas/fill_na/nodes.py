"""
This is a boilerplate pipeline 'fill_na'
generated using Kedro 0.18.9
"""

import pandas as pd
from typing import Dict


def fillna(dataset: pd.DataFrame, parameters: Dict) -> pd.DataFrame:
    return dataset.fillna(**parameters)
