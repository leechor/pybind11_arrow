import functools
import inspect
import re
from pathlib import Path

import pandas as pd
import pyarrow as pa
import python_example as m
from pandas import DataFrame

from src.app.tm.tm_frame import TmFrame
from src.app.tools.invoke_inject import invoke_by_json


def dataframe_to_arrow(df: DataFrame):
    return pa.Table.from_pandas(df)


def arrow_to_dataframe(table: pa.Table):
    return table.to_pandas()


def print_df(df: TmFrame):
    table = dataframe_to_arrow(df)
    m.print_table(table)


def read_tm_data(filepath_or_buffer: str):
    name = Path(filepath_or_buffer).name
    task, tm, start, end, _ = re.split(r'[\s至数]', name)
    data = pd.read_csv(filepath_or_buffer=filepath_or_buffer,
                       parse_dates=True,
                       index_col=0,
                       header=None,
                       usecols=[0, 1],
                       names=['time', tm, task])
    return TmFrame(data)


def convert_index_to_period(df):
    df_r = df
    if not isinstance(df.index, pd.PeriodIndex):
        df_r = df.copy()
        df_r.index = df.index.to_period(freq='S')
    return df_r


def join_tm_by_second(tms: list):
    def join(df, dfc):
        df_r = convert_index_to_period(df)
        dfc_r = convert_index_to_period(dfc)
        return pd.merge(df_r, dfc_r, on='time')

    result = functools.reduce(join, tms[1:], tms[0])
    return result


def read_tm_datas(file_paths: list[str]):
    data: TmFrame = None
    for file_path in file_paths:
        d = read_tm_data(file_path)
        data = pd.concat([data, d])
    return data


if __name__ == '__main__':
    arg = r"""
    {
     "name": "src.app.tm.pd_func.read_tm_datas",
     "args": [["C:/Users/hp/Nutstore/.nutstore_Y2hpbmFiaHN1bkBnbWFpbC5jb20=/record/2023/zdpx/XXXX TX05 20221226至20221228数据txt", 
     "C:/Users/hp/Nutstore/.nutstore_Y2hpbmFiaHN1bkBnbWFpbC5jb20=/record/2023/zdpx/XXXX TX05 20221226至20221228数据txt"]]
    }
    """
    sign = inspect.signature(invoke_by_json)
    result = invoke_by_json(arg)
    print(result)
