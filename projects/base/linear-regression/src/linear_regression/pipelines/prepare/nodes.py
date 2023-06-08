"""
This is a boilerplate pipeline 'prepare'
generated using Kedro 0.18.8
"""

import pandas as pd


def __process_boolean_encoded_column__(dataset):
    # Day with: Thunder; Sleet; Hail; Dust or Sand; Smoke or Haze; Blowing Snow; Rain; Snow; Glaze; Fog; Is Observed;
    # 0 = No, 1 = Yes
    max_len = 10 + 1
    column = 'TSHDSBRSGF'
    columns = ['thunder', 'sleet', 'hail', 'dust', 'smoke', 'blowing_snow', 'rain', 'snow', 'glaze', 'fog',
               'is_observed']

    def split_and_normalize(s):
        if s is None or isinstance(s, float):
            return [0] * max_len

        l = list(s)
        l = [0 if c == ' ' else int(c) for c in l]

        data_len = max_len - 1

        if len(l) < data_len:
            l += [0] * (data_len - len(l))

        l += [1]

        return l

    s = dataset[column].apply(split_and_normalize)

    new_df = pd.DataFrame(s.to_list(), index=s.index, columns=columns, dtype=bool)

    dataset = dataset.join(new_df)
    dataset = dataset.drop([column], axis=1)

    return dataset


def __encode_trace__(dataset, column, bool_column, value='T'):
    is_traceable = dataset[column] == value

    dataset.loc[is_traceable, column] = 0.0
    dataset[column] = dataset[column].astype(float)
    dataset[bool_column] = is_traceable.astype(bool)

    return dataset


def process(dataset: pd.DataFrame) -> pd.DataFrame:
    dataset = __encode_trace__(dataset, 'Precip', 'is_traceable_precip', value='T')
    dataset = __encode_trace__(dataset, 'Snowfall', 'is_traceable_snow', value='#VALUE!')
    dataset = __process_boolean_encoded_column__(dataset)

    return dataset
