import logging
import re

import numpy as np
import pandas as pd
from pandas import DataFrame
from simpleeval import SimpleEval

from src.app.tm.tm_frame import TmFrame


def parse_regular(expression: str):
    ex = re.sub('[$#]', '', expression)
    s = SimpleEval()
    parsed = s.parse(ex)

    def func(names: dict):
        s.names = names
        return s.eval(ex, previously_parsed=parsed)

    return func


def valid_expression(expression: str) -> str:
    ex = re.sub('[$#]', '', expression)
    s = SimpleEval()
    try:
        s.parse(ex)
        return None
    except SyntaxError as e:
        logging.error(f'{expression} expression syntax error, {e.msg}')
        return e.msg


def calculate_row(row, **kwargs):
    func = kwargs['indicator_func']
    nv = row.to_dict()
    return func(nv)


def extract_tm_variables(expression: str):
    tms = extract_variables(expression, r'\$\w+\d*')
    ts = [tm[1:] for tm in tms]
    return ts


def extract_indicator_variables(expression: str):
    ids = extract_variables(expression, r'#\w+\d*')
    idc = [ds[1:] for ds in ids]
    return idc


def extract_variables(expression: str, regrex: str):
    pattern = re.compile(regrex)
    return pattern.findall(expression)


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


def exec_regular_by_config(*args, context=None, **kwargs):
    tms = kwargs['tms']
    all_tm_result = context['all_tm_result']
    first_column = all_tm_result[0].iloc[:,:2]
    first_column.columns.values[0] = exec_regular_by_config.__name__
    return first_column


def test():
    ex = '$a + $a1 + $ab1 + $a1b + $a12+ $a12b + #a + #a1 + #ab1 + #a1b + #a12+ #a12b'
    print(extract_variables(ex))

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
    ex = '($Colorado > 0.3) and (#Texas < 0)'

    result = tf.exec_regular(ex)
    print(result)
