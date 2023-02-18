import functools
import types
from typing import Any

import numpy as np
import pandas as pd


def t(self: Any, name: str = '', *args, **kwargs):
    if getattr(self, name, False):
        # contains name
        result = getattr(self, name)(*args, **kwargs)
        if getattr(result, t.__name__, True):
            if isinstance(self, types.ModuleType):
                self.t = functools.partial(t, self)
            else:
                result.t = types.MethodType(t, result)
        return result

    if getattr(self, t.__name__, True):
        # no dot attribute
        if isinstance(self, types.ModuleType):
            self.t = functools.partial(t, self)
        else:
            self.t = types.MethodType(t, self)
        return self


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


if __name__ == '__main__':
    testDataFrame(np)
