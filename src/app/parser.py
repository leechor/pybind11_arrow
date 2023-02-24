import logging

import pandas as pd

from src.app.configure import Configure
from src.app.tm.tm_frame import TmFrame
from tools.invoke_inject import invoke_m, get_module_func_name

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


def process(config: Configure):
    for flow in config.flows:
        pre_result = None
        for func in flow.functions:
            logging.info(f'{func.name} and {func.description}')
            module, func_name = get_module_func_name(func.name)
            if module is not None:
                pre_result = module

            args = func.args if func.args else []
            kwargs = func.kwargs.__dict__ if func.kwargs else {}

            pre_result = invoke_m(pre_result, func_name, *args, **kwargs)

            if isinstance(pre_result, pd.DataFrame):
                pre_result = TmFrame(pre_result)


if __name__ == '__main__':
    process(Configure.load(config))

