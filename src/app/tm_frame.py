import functools

import pandas as pd

from tools.invoke_inject import inject_method, invoke_m


def get_klas_methods(target):
    """ based on https://stackoverflow.com/a/34452 """
    all_methods = [
        method_name for method_name in dir(target)
        if callable(getattr(target, method_name)) and method_name[0:2] != "__" and method_name[0:1] != "_"
    ]
    return all_methods


def for_all_methods(decorator):
    def decorate(cls):
        for attr in get_klas_methods(cls):
            if callable(getattr(cls, attr)):
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls

    return decorate


def convert_to_tm_frame(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, pd.DataFrame):
            result = TmFrame(result)
        return result

    return decorator


@for_all_methods(convert_to_tm_frame)
class TmFrame(pd.DataFrame):
    pass


inject_method(TmFrame, invoke_m)
