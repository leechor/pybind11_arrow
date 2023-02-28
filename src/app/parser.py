import json
import logging
from pathlib import Path

import pandas as pd
from jsonpath_ng import parse

from src.app.configure import Configure
from src.app.tm.regular import extract_tm_variables, extract_indicator_variables
from src.app.tm.tm_frame import TmFrame
from src.app.tools.module_loading import load_module
from tools.invoke_inject import invoke_m, get_module_func_name

FUNCTIONS = 'functions'

DESCRIPTION = 'description'

NAME = 'name'

REGULAR = 'regular'

INDICATOR = 'indicator'

TM = 'tm'

TYPE = 'type'

config = '''
{
    "name": "名称",
    "description": "这一级别用来表示这个配置文件的整体信息",
    "flows": [
    {
        "name": "TM1",
        "type": "tm",
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
        "type": "tm",
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
    """
    解析执行配置文件
    :param config:
    :return:
    """
    context = {'all_tm_result': [], 'all_indicator_result': [], 'all_regular_result': []}
    for flow in config.flows:
        pre_result = None
        for func in flow.functions:
            logging.info(f'{func.name} and {func.description}')
            module, func_name = get_module_func_name(func.name)
            if module is not None:
                pre_result = module

            args = func.args if func.args else []
            kwargs = func.kwargs.__dict__ if func.kwargs else {}

            kwargs['context'] = context

            pre_result = invoke_m(pre_result, func_name, *args, **kwargs)

            if isinstance(pre_result, pd.DataFrame):
                pre_result = TmFrame(pre_result)

        if pre_result is not None:
            if flow.type == TM:
                context['all_tm_result'].append(pre_result)
            elif flow.type == INDICATOR:
                context['all_indicator_result'].append(pre_result)
            elif flow.type == REGULAR:
                context['all_regular_result'].append(pre_result)

    return context


all_config = """
{
  "task": "task name",
  "description": "这一级别用来表示这个配置文件的整体信息",
  "regulars": ["$TM1 + $TM2 + #indicator_1", "$TM1 + #indicator_2 + #indicator_1"],
  "indicators": [
    {
      "name": "D:/project/python_example/src/temp/indicator_1.py",
      "args": [],
      "kwargs": {
        "filepath_or_buffer": "D:/XXXX TX01 20221226至20221228数据txt"
      },
      "description": ""
    },
    {
      "name": "D:/project/python_example/src/temp/indicator_2.py",
      "args": [],
      "kwargs": {
        "filepath_or_buffer": "D:/XXXX TX02 20221226至20221228数据txt"
      },
      "description": ""
    }
  ],
  "preprocess": {
    "name": "名称",
    "description": "这一级别用来表示这个配置文件的整体信息",
    "flows": [
      {
        "name": "TM1",
        "description": "这一级别用来表示某个参数处理的信息",
        "functions": [
          {
            "name": "src.app.tm.pd_func.read_tm_data",
            "args": [],
            "kwargs": {
              "filepath_or_buffer": "D:/XXXX TX01 20221226至20221228数据txt"
            },
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
          }
        ]
      },
      {
        "name": "TM2",
        "functions": [
          {
            "name": "src.app.tm.pd_func.read_tm_data",
            "args": ["D:/XXXX TX02 20221226至20221228数据txt"],
            "kwargs": null,
            "description": "some information"
          }
        ]
      }
    ]
  }
}

"""


def parse_calc_flows(al: str):
    j = json.loads(al)

    regulars: list = get_regulars(j)
    tms, ids = get_regular_variables(regulars)

    # tm
    func_flows = get_Tms(j, tms)

    # indicator

    indicator_expr = parse('$.indicators[*]')
    idcs = [v.value for v in indicator_expr.find(j)]
    for idc in idcs:
        name = idc[NAME]
        # todo
        load_module(name)
        module_name = Path(name).stem
        idc[NAME] = f'{module_name}.indicate'
        indicator_functions = {NAME: module_name, TYPE: INDICATOR, FUNCTIONS: [idc]}
        func_flows.append(indicator_functions)

    # regular
    for regular in regulars:
        tms, ids = get_regular_variables([regular])

        r = {
            NAME: 'src.app.tm.regular.exec_regular_by_config',
            DESCRIPTION: regular,
            'args': None,
            'kwargs': {
                'tms': tms,
                'indicators': ids
            }}
        indicator_functions = {NAME: 'regular', TYPE: REGULAR, FUNCTIONS: [r]}
        func_flows.append(indicator_functions)

    result = {}
    result[NAME] = parse('$.task').find(j)[0].value
    result[DESCRIPTION] = parse('$.description').find(j)[0].value
    result['flows'] = func_flows
    js = json.dumps(result, ensure_ascii=False)
    return js


def get_Tms(j, tms):
    tms_pre_expr = parse('$.preprocess.flows[*]')
    tms_pre = [v.value for v in tms_pre_expr.find(j) if v.value['name'] in tms]
    for tp in tms_pre:
        tp[TYPE] = 'tm'
    return tms_pre


def get_regular_variables(regulars):
    tms = set()
    ids = set()
    for regular in regulars:
        tm = extract_tm_variables(regular)
        tms = tms.union(tm)

        indicate = extract_indicator_variables(regular)
        ids = ids.union(indicate)
    return list(tms), list(ids)


def get_regulars(j):
    regulars_expr = parse('regulars[*]')
    regulars = [v.value for v in regulars_expr.find(j)]
    return regulars


def testProcess():
    process(Configure.load(config))


if __name__ == '__main__':
    js = parse_calc_flows(all_config)
    cf = 'd:/config.json'
    with open(cf, 'w') as f:
        f.write(js)

    with open(cf) as f:
        js = f.read()
        process(Configure.load(js))

