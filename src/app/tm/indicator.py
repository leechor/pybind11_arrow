import logging
import re

import numpy as np
import pandas as pd
from pandas import DataFrame
from simpleeval import SimpleEval

from src.app import TmFrame, inject_method


def parse_regular(expression: str):
    ex = re.sub('[$#]', '', expression)
    s = SimpleEval()
    parsed = s.parse(ex)

    def func(names: dict):
        s.names = names
        return s.eval(ex, previously_parsed=parsed)

    return func


def valid_expression(expression: str):
    ex = re.sub('[$#]', '', expression)
    s = SimpleEval()
    try:
        s.parse(ex)
    except SyntaxError as e:
        logging.error(f'{expression} expression syntax error, {e.msg}')


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


def exec_regular(df: DataFrame, expression: str):
    """
    根据规则运算逻辑, 运行数据过滤
    :param df: self
    :param expression: 规则运算逻辑表达式, 需要符合python语法
    :return:
    """
    func = parse_regular(expression)
    frame = df.apply(calculate_row, axis=1, indicator_func=func)
    return tf[frame]


inject_method(TmFrame, exec_regular)

if __name__ == '__main__':
    tf = TmFrame(np.random.standard_normal((2, 4)),
                 index=pd.date_range("2000-01-01", periods=2,
                                     freq="W-WED"),
                 columns=["Colorado", "Texas", "NewYork", "Ohio"])
    print(tf.head())
    ex = '($Colorado > 0.3) and (#Texas < 0)'

    result = tf.exec_regular(ex)
    print(result)
