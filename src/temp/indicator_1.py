from src.app.tm.pd_func import read_tm_data


def indicate(*args, **kwargs):
    return read_tm_data(kwargs['filepath_or_buffer'])
