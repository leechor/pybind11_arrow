import pandas as pd
import python_example as m
from pandas import DataFrame

assert m.__version__ == '0.0.1'
assert m.add(1, 2) == 3
assert m.subtract(1, 2) == -1
assert m.mul(2, 3) == 6


def identify(f: DataFrame) -> DataFrame:
    return m.printDf(f)


def test():
    m.invoke_m(None, "print", 123)


def valid_regular():
    global data
    data = {"state": ["Ohio", "Ohio", "Ohio", "Nevada", "Nevada", "Nevada"],
            "year": [2000, 2001, 2002, 2001, 2002, 2003],
            "pop": [1.5, 1.7, 3.6, 2.4, 2.9, 3.2]}
    df = pd.DataFrame(data)
    # identify(df)
    # m.testDataFrameC()
    result = m.valid_regular_expression('($Colorado > 0.3) and (#Texas < 0)')
    print(result)


if __name__ == '__main__':
    df = m.read_csv(r'D:/project/python_example/src/stock_2.csv')
    print(df)

