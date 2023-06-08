"""
This is a boilerplate pipeline 'date_to_float'
generated using Kedro 0.18.9
"""

import numpy as np
import pandas as pd


def convert_date_to_float(dataset, parameters):
    columns = parameters['columns']
    normalize = parameters['normalize']

    for column in columns:
        series = dataset[column]

        if not pd.api.types.is_datetime64_any_dtype(series):
            series = pd.to_datetime(series, errors='coerce')

        year = series.dt.year
        day = series.dt.day_of_year
        number_of_days_in_year = (series + pd.offsets.YearEnd()).dt.day_of_year
        date = day / number_of_days_in_year

        match normalize:
            case 'skip':
                pass
            case 'index_by_year':
                date = (year.astype(float) - year.min()) + date
            case 'no':
                date = year.astype(float) + date
            case _:
                raise ValueError(f'Unknown normalize option: { normalize }')

        dataset[column] = date

    return dataset

