import json
import re
from pathlib import Path

import pandas as pd
import pyarrow as pa
import python_example as m
from pandas import DataFrame

from src.app.tools.invoke_inject import inject_method, invoke_m, get_module_func_name
from src.app.tm_frame import TmFrame


def dataframe_to_arrow(df: DataFrame):
    return pa.Table.from_pandas(df)


def arrow_to_dataframe(table: pa.Table):
    return table.to_pandas(table)


def print_df(df: TmFrame):
    table = dataframe_to_arrow(df)
    m.print_table(table)


def read_tm_data(file_path: str):
    name = Path(file_path).name
    task, tm, start, end, _ = re.split(r'[\s至数]', name)
    data = pd.read_csv(file_path,
                       parse_dates=True,
                       index_col=0,
                       header=None,
                       usecols=[0, 1],
                       names=['time', tm, task])
    return TmFrame(data)


class Argument:
    def __init__(self, d):
        self.__dict__ = d

    def __getattr__(self, item):
        pass


def invoke_by_json(arg: str):
    argument = json.loads(arg, object_hook=Argument)
    module_name, func_name = get_module_func_name(argument.name)
    args = argument.args if argument.args else []
    kwargs = argument.kwargs.__dict__ if argument.kwargs else {}
    return invoke_m(module_name, func_name, *args, **kwargs)


inject_method(TmFrame, dataframe_to_arrow)


if __name__ == '__main__':
    arg = r'{"name": "src.app.tm.pd_func.read_tm_data", "args": ["C:/Users/hp/Nutstore/.nutstore_Y2hpbmFiaHN1bkBnbWFpbC5jb20=/record/2023/zdpx/XXXX TX05 20221226至20221228数据txt"]}'
    result = invoke_by_json(arg)
    print(result)
