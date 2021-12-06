import os
from typing import Optional, Union

import yaml

config: Optional[dict[str, dict[str, Union[int, str]]]] = None


def config_init():
    '''初始化config'''
    global config
    with open('config.yml', 'r', encoding='utf-8') as f:
        cfg = f.read()
        config = yaml.load(cfg, Loader=yaml.FullLoader)

    # 判断项目目录是否存在
    data = config['data']['path']
    if not os.path.exists(data):
        os.makedirs(data)
