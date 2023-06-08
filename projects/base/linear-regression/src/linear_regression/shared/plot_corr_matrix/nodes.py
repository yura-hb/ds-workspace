"""
This is a boilerplate pipeline 'plot_corr_matrix'
generated using Kedro 0.18.9
"""

import pandas as pd
import numpy as np
import plotly.figure_factory as ff

from typing import Dict


def plot_corr_matrix(dataset: pd.DataFrame, parameters: Dict):
    all = parameters.get('all') or False

    df = dataset

    if not all:
        columns = list(set(parameters['columns']).intersection(dataset.columns))
        df = df[columns]

    method = parameters.get('method') or 'pearson'
    round_positions = parameters.get('round_positions') or 2

    corr_matrix = df.corr(method)

    values = np.around(corr_matrix.values.tolist(), round_positions)

    fig = ff.create_annotated_heatmap(
        z=corr_matrix.values.tolist(),
        x=corr_matrix.columns.tolist(),
        y=corr_matrix.columns.tolist(),
        annotation_text=values,
        hoverinfo='z',
        showscale=True
    )

    return fig
