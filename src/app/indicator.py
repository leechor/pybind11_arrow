import re

import numpy as np
import pandas as pd
from simpleeval import SimpleEval

from src.app import TmFrame


def parse_regular(expression: str):
    ex = re.sub('[$#]', '', expression)
    s = SimpleEval()
    parsed = s.parse(ex)

    def func(names: dict):
        s.names = names
        return s.eval(ex, previously_parsed=parsed)

    return func


def calculate_row(row, **kwargs):
    func = kwargs['indicator_func']
    nv = row.to_dict()
    return func(nv)


def extract_tm_variables(expression: str):
    return extract_variables(expression, r'\$\w+\d*')


def extract_indicator_variables(expression: str):
    return extract_variables(expression, r'#\w+\d*')


def extract_variables(expression: str, regrex: str):
    pattern = re.compile(regrex)
    return pattern.findall(expression)


def test():
    ex = '$a + $a1 + $ab1 + $a1b + $a12+ $a12b + #a + #a1 + #ab1 + #a1b + #a12+ #a12b'
    print(extract_variables(ex))


def test2():
    ex = '$a + #b'
    pi = parse_regular(ex)
    print(pi({'a': 1, 'b': 2}))
    print(pi({'a': 4, 'b': 5}))


if __name__ == '__main__':
    tf = TmFrame(np.random.standard_normal((2, 4)),
                 index=pd.date_range("2000-01-01", periods=2,
                                     freq="W-WED"),
                 columns=["Colorado", "Texas", "NewYork", "Ohio"])
    print(tf.head())
    ex = '($Colorado > 3.3) and ((#Texas > 0.7) or (#Ohio < 5) or (#NewYork < 0.3))'
    func = parse_regular(ex)
    frame = tf.apply(calculate_row, axis=1, indicator_func=func)
    print(frame.head())
