

import inspect

def load_class(module, key):
    pass


def load_constructor(cls) -> inspect.Signature:
    return inspect.Signature(cls.__init__)
