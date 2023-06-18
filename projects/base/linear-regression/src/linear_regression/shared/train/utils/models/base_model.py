

from abc import ABC, abstractmethod
from collections import OrderedDict
from typing import Tuple, Dict

import sklearn.metrics

from ..reflection_utils import load_obj


class BaseModel(ABC):

    def __init__(self, parameters, metrics, configuration):
        self.parameters = parameters
        self.metrics_ids = metrics
        self.configuration = configuration
        self.evaluated_metrics = None

    @abstractmethod
    def train(self, X_train, X_test, y_train, y_test):
        pass

    @property
    @abstractmethod
    def metrics(self) -> Dict:
        pass

    @property
    @abstractmethod
    def ordered_metrics(self) -> Tuple:
        pass

    @property
    @abstractmethod
    def base_model(self):
        pass

    @staticmethod
    def __evaluate_metrics__(prediction, target, metrics, configuration):
        result = OrderedDict()

        for metric_id, params in metrics.items():
            params = (params or dict()).copy()
            components = metric_id.split('.')
            prefix, metric_name = components[0], '.'.join(components[1:])

            if 'class' in params:
                metric_name = params['class']
                del params['class']

            match prefix:
                case 'sklearn':
                    scorer = load_obj(sklearn.metrics, metric_name)

                    result[metric_id] = scorer(target, prediction, **params)
                case 'custom':
                    scorer = configuration.metrics[metric_name]
                    value = scorer(target, prediction, **params)

                    if isinstance(value, OrderedDict):
                        for key, item in value.items():
                            result[metric_id + '.' + key] = item
                    else:
                        result[metric_id] = value
                case '_':
                    raise ValueError('Unknown metric prefix')

        return result
