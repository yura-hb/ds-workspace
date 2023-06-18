import importlib
import inspect


def load_obj(module, key):
    """
    Loads class directly from module

    Args:
        module: Module object
        key: Class key

    Returns: A class prototype
    """
    return getattr(module, key)


def load_nested_class(path):
    components = path.split('.')

    module = '.'.join(components[:-1])
    module = importlib.import_module(module)

    key = components[-1]

    return load_obj(module, key)


def load_constructor(cls) -> inspect.Signature:
    return inspect.signature(cls.__init__)
