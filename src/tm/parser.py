import json


config = '''
{
    "name": "名称",
    "description": "这一级别用来表示这个配置文件的整体信息",
    "flows": [
    {
        "name": "TM1",
        "description": "这一级别用来表示某个参数处理的信息",
        "functions": [{
            "name": "load_data",
            "args": [["full_name1", "full_name2"]],
            "kwargs": {"k1": "v1", "k2": "v2"},
            "description": "函数表示每个处理步骤, 如加载数据函数, 每个函数的默认输出为dataframe, 默认作为下一个函数的第一个函数"
        },
        {
            "name": "function1",
            "args": [["full_name1", "full_name2"]],
            "kwargs": {"k1": "v1", "k2": "v2"},
            "description": "函数表示每个处理步骤, 如加载数据函数, 每个函数的默认输出为dataframe, 默认作为下一个函数的第一个函数"
        }]

    },
    {
        "name": "TM2",
        "functions": [{
            "name": "function2",
            "args": ["arg1", "arg2"],
            "kwargs": {"k1": "v1", "k2": "v2"},
            "description": "some information"
        },
        {
            "name": "function3",
            "args": ["arg1", "arg2"],
            "kwargs": {"k1": "v1", "k2": "v2"},
            "description": "some information"
        }
    ]
    },
    {
        "name": "output",
        "functions": [{
            "name": "convertToArrow",
            "args": [],
            "kwargs": {},
            "description": "convert dataframe format to arrow format"
        }]
    }
    ]
}


'''


class Configure:
    def __init__(self, d):
        self.name = None
        self.description = None
        self.flows = None
        self.__dict__ = d

    @classmethod
    def load(cls, config: str):
        return json.loads(config, object_hook=Configure)


def process(config: Configure):
    for flow in config.flows:
        for func in flow.functions:
            print(f'{func.name} and {func.description}')


if __name__ == '__main__':
    process(Configure.load(config))
