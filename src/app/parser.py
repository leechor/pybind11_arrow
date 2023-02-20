import json
import logging

import numpy as np
import pandas as pd

from tm import print_df
from tm_frame import TmFrame
from tools.invoke_inject import invoke_m, inject_method
from tools.module_loading import module_import

config = '''
{
    "name": "名称",
    "description": "这一级别用来表示这个配置文件的整体信息",
    "flows": [
    {
        "name": "TM1",
        "description": "这一级别用来表示某个参数处理的信息",
        "functions": [{
            "name": "pandas.read_csv",
            "args": [],
            "kwargs": {"filepath_or_buffer": "D:/project/python_example/src/stock_1.csv"},
            "description": "函数表示每个处理步骤, 如加载数据函数, 每个函数的默认输出为dataframe, 默认作为下一个函数的第一个函数"
        },
        {
            "name": "head",
            "args": [6],
            "kwargs": null,
            "description": "函数表示每个处理步骤, 如加载数据函数, 每个函数的默认输出为dataframe, 默认作为下一个函数的第一个函数"
        },
                {
            "name": "head",
            "args": [4],
            "kwargs": null,
            "description": "函数表示每个处理步骤, 如加载数据函数, 每个函数的默认输出为dataframe, 默认作为下一个函数的第一个函数"
        },
        {
            "name": "print_df",
            "args": [],
            "kwargs": {},
            "description": "函数表示每个处理步骤, 如加载数据函数, 每个函数的默认输出为dataframe, 默认作为下一个函数的第一个函数"
        }]
    },
    {
        "name": "TM2",
        "functions": [{
            "name": "pandas.read_csv",
            "args": ["D:/project/python_example/src/stock_2.csv"],
            "kwargs": null,
            "description": "some information"
        }
    ]
    }
    ]
}

'''


class Flow:
    def __init__(self, d):
        self.name = None
        self.description = None


class Configure:
    def __init__(self, d):
        self.name = None
        self.description = None
        self.flows: list = []
        self.__dict__ = d

    @classmethod
    def load(cls, config: str):
        return json.loads(config, object_hook=Configure)


def process(config: Configure):
    for flow in config.flows:
        pre_result = None
        for func in flow.functions:
            logging.info(f'{func.name} and {func.description}')
            func_name = ""
            if '.' in func.name:
                n = func.name
                pre_result = module_import(n[:n.index('.')])
                func_name = n[n.index('.') + 1:]
            else:
                func_name = func.name

            args = func.args if func.args else []
            kwargs = func.kwargs.__dict__ if func.kwargs else {}

            pre_result = invoke_m(pre_result, func_name, *args, **kwargs)

            if isinstance(pre_result, pd.DataFrame):
                pre_result = TmFrame(pre_result)


def testDataFrame(n):
    data = TmFrame(n.random.standard_normal((2, 4)),
                   index=pd.date_range("2000-01-01", periods=2,
                                       freq="W-WED"),
                   columns=["Colorado", "Texas", "New York", "Ohio"])
    df = TmFrame(data)
    print(invoke_m(df).invoke_m('resample', 'D').invoke_m('asfreq'))


def test2():
    a = invoke_m(np.random, 'standard_normal', (2, 4))
    index = invoke_m(pd, 'date_range', '2000-01-01', periods=2, freq="W-WED")
    frame = invoke_m(pd, "DataFrame", a,
                     index=index,
                     columns=["Colorado", "Texas", "New York", "Ohio"])
    print(frame)


def test3():
    a = invoke_m(None, 'test2')
    print(a)


if __name__ == '__main__':
        # test2()
        # testDataFrame(np)
    inject_method(TmFrame, print_df)
    process(Configure.load(config))
    tf = TmFrame(np.random.standard_normal((2, 4)),
                 index=pd.date_range("2000-01-01", periods=2,
                                     freq="W-WED"),
                 columns=["Colorado", "Texas", "New York", "Ohio"])
    tf.head(6).head(4).print_df()
