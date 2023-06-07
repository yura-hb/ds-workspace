"""
This is a boilerplate pipeline 'make_info'
generated using Kedro 0.18.9
"""

import io
import pandas as pd
from typing import Dict


def make_info(dataset: pd.DataFrame, parameters: Dict) -> str:
    buf = io.StringIO()

    dataset.info(buf=buf, **parameters)

    return buf.getvalue()
