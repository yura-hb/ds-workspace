"""
This is a boilerplate pipeline 'fold_split'
generated using Kedro 0.18.9
"""

import logging

from sklearn.model_selection import KFold, StratifiedKFold, StratifiedGroupKFold, GroupKFold

log = logging.getLogger(__name__)

def __make_split__(split_class, n_folds, parameters):
    return split_class(n_splits=n_folds, **parameters)


def __make_fold_split__(X, y, parameters, n_folds: int = 1):
    group_column = parameters.get('group_column')
    stratify = parameters.get('stratify') or False

    if stratify:
        del parameters['stratify']

    if group_column is not None:
        del parameters['group_column']

    if group_column is not None:
        groups = X[group_column]

        if "shuffle" in parameters.keys() or "random_state" in parameters.keys():
            log.warning("Grouped KFold doesn't support shuffling")

        return __make_split__(StratifiedGroupKFold if stratify else GroupKFold, n_folds, dict()), (X, y, groups)

    return __make_split__(StratifiedKFold if stratify else KFold, n_folds, parameters), (X, y)


def split(X, y, parameters, n_folds: int = 1):
    fold_split, split_data = __make_fold_split__(X, y, parameters, n_folds)
    out = []

    for train_idx, test_idx in fold_split.split(X, y):
        X_train, X_val, y_train, y_val = X.iloc[train_idx, :], X.iloc[train_idx, :], y.iloc[test_idx, :], y.iloc[test_idx, :]

        out += [X_train, X_val, y_train, y_val]

    return out
