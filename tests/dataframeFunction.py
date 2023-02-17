import functools
import types
from typing import Any

import numpy as np
import pandas as pd


def dot(self: Any, name: str = None, *args, **kwargs):
    if getattr(self, name, False):
        # contains name
        result = getattr(self, name)(*args, **kwargs)
        if getattr(result, dot.__name__, True):
            if isinstance(self, types.ModuleType):
                self.dot = functools.partial(dot, self)
            else:
                result.dot = types.MethodType(dot, result)
        return result

    if getattr(self, dot.__name__, True):
        # no func attribute
        if isinstance(self, types.ModuleType):
            self.dot = functools.partial(dot, self)
        else:
            self.dot = types.MethodType(dot, self)
        return self


def testDataFrame(n):
    data = pd.DataFrame(n.random.standard_normal((2, 4)),
                        index=pd.date_range("2000-01-01", periods=2,
                                            freq="W-WED"),
                        columns=["Colorado", "Texas", "New York", "Ohio"])
    df = pd.DataFrame(data)
    print(dot(df, "").dot('resample', 'D').dot('asfreq'))


def test2():
    a = dot(np.random, 'standard_normal', (2, 4))
    index = dot(pd, 'date_range', '2000-01-01', periods=2, freq="W-WED")
    frame = dot(pd, "DataFrame", a,
                index=index,
                columns=["Colorado", "Texas", "New York", "Ohio"])
    print(frame)


if __name__ == '__main__':
    testDataFrame(np)
