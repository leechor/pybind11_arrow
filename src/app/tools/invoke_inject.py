import builtins
import inspect
import json
import logging
import sys
import types
import typing
from typing import Any, Callable

from src.app.tools.module_loading import module_import


def invoke_m(target: Any, name: str = None, *args, **kwargs):
    """
    调用方法到target
    :param target: 可以是module/class
    :param name: 函数名
    :param args: 参数列表
    :param kwargs: 字典类型参数集合
    :return: None
    """
    if target is None:
        target = builtins

    inject_method(target, invoke_m)
    if name is not None:
        if getattr(target, name, False):
            func = getattr(target, name)
            spec = inspect.getfullargspec(func)
            if 'context' not in spec.kwonlyargs:
                del kwargs['context']
            result = func(*args, **kwargs)
            inject_method(result, invoke_m)
            return result
        else:
            logging.warning(f"{target}.{name} not exist")
    return target


def inject_method_by_name(target: Any, func_name: str):
    current_module = sys.modules[__name__]
    if getattr(current_module, func_name, False):
        func = getattr(current_module, func_name)
        inject_method(target, func)


def inject_method(target: Any, f: Callable):
    if target is None or getattr(target, f.__name__, False):
        return

    try:
        if isinstance(target, type | types.ModuleType):
            setattr(target, f.__name__, f)
        else:
            setattr(target, f.__name__, types.MethodType(f, target))
    except Exception as e:
        # type maybe immutable
        logging.warning(e)
        pass


def get_function_by_name(name: str):
    if name is not None:
        module, func_name = get_module_func_name(name)

        if getattr(module, func_name, False):
            func = getattr(module, func_name)
            return func


def get_module_func_name(name: str):
    r = name.rsplit('.', 1)
    if len(r) == 1:
        return None, r[0]
    else:
        return module_import(r[0]), r[1]


class Argument:
    def __init__(self, d):
        self.__dict__ = d

    def __getattr__(self, item):
        pass


def invoke_by_json(arg: str):
    argument = json.loads(arg, object_hook=Argument)
    module_name, func_name = get_module_func_name(argument.name)
    args = argument.args if argument.args else []
    kwargs = argument.kwargs.__dict__ if argument.kwargs else {}
    return invoke_m(module_name, func_name, *args, **kwargs)


def get_func_arguments_by_name(name: str):
    func = get_function_by_name(name)
    if func is not None:
        func = get_func_arguments(func)
        return func.args


def get_func_arguments(func: typing.Callable):
    return inspect.getfullargspec(func)


if __name__ == '__main__':
    func = get_func_arguments_by_name('src.app.tools.invoke_inject.invoke_m')
    print(func)