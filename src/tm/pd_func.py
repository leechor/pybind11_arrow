import pyarrow as pa
import python_example as m
from pandas import DataFrame


def dataframe_to_arrow(df: DataFrame):
    return pa.Table.from_pandas(df)


def arrow_to_dataframe(table: pa.Table):
    return table.to_pandas(table)


def print_df(df: DataFrame):
    table = dataframe_to_arrow(df)
    m.print_table(table)
