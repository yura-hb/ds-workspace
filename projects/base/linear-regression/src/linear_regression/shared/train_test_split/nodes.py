"""
This is a boilerplate pipeline 'train_test_split'
generated using Kedro 0.18.9
"""

from sklearn.model_selection import train_test_split


def split(*arrays):
    datasets = arrays[:-1]
    parameters = arrays[-1]

    return train_test_split(*datasets, **parameters)

