import os

from src.app.tm.pd_func import read_tm_data


def indicate(*args, **kwargs):
    df = read_tm_data(kwargs['filepath_or_buffer'])
    file_name, _ = os.path.basename(__file__).split('.')
    df.columns.values[0] = file_name
    return df
