"""
This is a boilerplate pipeline 'fold_split'
generated using Kedro 0.18.9
"""

from sklearn.model_selection import KFold


def split(X, y, parameters, n_folds: int = 1):
    fold_split = KFold(n_splits=n_folds, **parameters)
    out = []

    for train_idx, test_idx in fold_split.split(X, y):
        X_train, X_val, y_train, y_val = X.iloc[train_idx, :], X.iloc[train_idx, :], y.iloc[test_idx, :], y.iloc[test_idx, :]

        out += [X_train, X_val, y_train, y_val]

    return out
