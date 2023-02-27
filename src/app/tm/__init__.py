from src.app.tm.regular import exec_regular
from src.app.tm.pd_func import print_df, dataframe_to_arrow
from src.app.tm.tm_frame import TmFrame
from src.app.tools.invoke_inject import inject_method, invoke_m

tm_function = [invoke_m, print_df, dataframe_to_arrow, exec_regular]

for func in tm_function:
    inject_method(TmFrame, func)
