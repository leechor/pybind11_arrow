import builtins
import sys
import types
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
            result = func(*args, **kwargs)
            inject_method(result, invoke_m)
            return result
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
    except Exception:
        # type maybe immutable
        pass


def get_module_func_name(name: str):
    module_name = None
    func_name = ""
    if '.' in name:
        n = name
        point_pos = n.rindex('.')
        module_name = module_import(n[:point_pos])
        func_name = n[point_pos + 1:]
    else:
        func_name = name
    return module_name, func_name
