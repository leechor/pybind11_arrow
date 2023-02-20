import sys
from typing import Any, Callable

import numpy as np
import pandas as pd


def t(target: Any, name: str = None, *args, **kwargs):
    """
    调用方法到target
    :param target: 可以是module/class
    :param name: 函数名
    :param args: 参数列表
    :param kwargs: 字典类型参数集合
    :return: None
    """
    current_module = sys.modules[__name__]
    if target is None:
        target = current_module

    if name is not None and getattr(target, name, False):
        func = getattr(target, name)
        result = func(*args, **kwargs)
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

    setattr(target, f.__name__, f)


def testDataFrame(n):
    data = pd.DataFrame(n.random.standard_normal((2, 4)),
                        index=pd.date_range("2000-01-01", periods=2,
                                            freq="W-WED"),
                        columns=["Colorado", "Texas", "New York", "Ohio"])
    df = pd.DataFrame(data)
    print(t(df).t('resample', 'D').t('asfreq'))


def test2():
    a = t(np.random, 'standard_normal', (2, 4))
    index = t(pd, 'date_range', '2000-01-01', periods=2, freq="W-WED")
    frame = t(pd, "DataFrame", a,
              index=index,
              columns=["Colorado", "Texas", "New York", "Ohio"])
    print(frame)


def test3():
    a = t(None, 'test2')
    print(a)


if __name__ == '__main__':
    testDataFrame(np)
