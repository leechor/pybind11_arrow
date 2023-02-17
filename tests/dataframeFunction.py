import types
from typing import Any

import numpy as np
import pandas as pd


def func(self: Any, name: str, *args, **kwargs):
    if getattr(self, name, False):
        # contains name
        result = getattr(self, name)(*args, **kwargs)
        if getattr(result, func.__name__, True):
            result.func = types.MethodType(func, result)
        return result
    elif getattr(self, func.__name__, True):
        # no func attribute
        self.func = types.MethodType(func, self)
        return self

def testDataFrame():
    data = pd.DataFrame(np.random.standard_normal((2, 4)),
                        index=pd.date_range("2000-01-01", periods=2,
                                            freq="W-WED"),
                        columns=["Colorado", "Texas", "New York", "Ohio"])
    df = pd.DataFrame(data)
    print(func(df, "").func('resample', 'D').func('asfreq'))


if __name__ == '__main__':
    pd = func(pd, '')
    np = func(np, '')
    frame = pd.func("DataFrame", np.func("random").func('standard_normal', (2, 4)),
                    index=pd.func('2000-01-01', periods=2, freq="W-WED"),
                    columns=["Colorado", "Texas", "New York", "Ohio"])
    print(frame)
