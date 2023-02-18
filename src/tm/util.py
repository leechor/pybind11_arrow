import sys
import types
from typing import Any, Callable

import numpy as np
import pandas as pd


def t(self: Any, name: str = None, *args, **kwargs):
    if self is None:
        self = sys.modules[__name__]

    if name is not None and getattr(self, name, False):
        # contains name
        func = getattr(self, name)
        result = func(*args, **kwargs)
        inject_t(result, t)
        return result
    inject_t(self, t)
    return self


def inject_t(target: Any, f: Callable):
    if getattr(target, t.__name__, False):
        return

    if isinstance(target, types.ModuleType):
        setattr(target, f.__name__, f)
    else:
        setattr(target, f.__name__, types.MethodType(f, target))
        # result.t = types.MethodType(t, result)

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
