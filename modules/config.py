import os
import json


def read_config():
    config_path = "config.json"
    if os.path.exists(config_path):
        print("√ 找到配置文件, 将从配置文件读取信息！")
        with open(config_path, encoding="utf-8") as f:
            config = f.read()
    else:
        print("X 配置文件不存在, 尝试从环境变量读取信息。")
        env_config = os.environ.get("CONFIG", "")
        if env_config:
            print("√ 环境变量 CONFIG 已设置, 正在解析匹配参数......")
            return json.loads(env_config)
        else:
            print("X 环境变量 CONFIG 未设置或为空。")
            return {}
    try:
        return json.loads(config)
    except json.JSONDecodeError as e:
        print("X JSON配置解析失败: ", e)
        return {}
