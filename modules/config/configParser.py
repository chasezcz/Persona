'''
@File    :   configParser.py
@Time    :   2020/12/02 14:59:45
@Author  :   Chengze Zhang 
@Contact :   chengze1996@gmail.com
@License :   Copyright (c) 2020 Chengze Zhang
'''

# here put the import lib
import json

def getAll(filepath):
    """
    Get all config value
    """
    with open(filepath, "r", encoding="utf-8") as target:
        return json.load(target)

def getValue(key, filepath="config.json"):
    config = getAll(filepath)
    # print(type(config))
    return config[key] if key in config else None

def putValue(key, value, filepath="config.json"):
    """
    Add or update value of config json.
    """
    config = getAll(filepath)
    config[key] = value
    with open("config.json", "w", encoding="utf-8") as target:
        target.write(json.dumps(config))

if __name__ == "__main__":
    print(putValue("datapath", "fjewf"))

