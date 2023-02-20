import json
import logging

from src import *
from src.tm.module_loading import import_string, module_import

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
            "args": [2],
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
        self.flows: list = None
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
            inject_method_by_name(pre_result, func_name)
            pre_result = t(pre_result, func_name, *args, **kwargs)


if __name__ == '__main__':
    process(Configure.load(config))
