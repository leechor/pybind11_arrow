import json


class Configure:
    def __init__(self, d):
        self.name = None
        self.description = None
        self.flows: list = []
        self.__dict__ = d

    @classmethod
    def load(cls, config: str):
        return json.loads(config, object_hook=Configure)

    def __getattr__(self, item):
        pass

class Flow:
    def __init__(self, d):
        self.name = None
        self.description = None

    def __getattr__(self, item):
        pass


def parse_tm_pre_flow(tm):
    """
    tm 格式 {"name": "TM_N", file_paths: [file1_path, file2_path], }
    结果也使用TM_N 表示
    :param tm: 遥测相关信息
    :return: 遥测预处理流程解析配置
    """
    pass

