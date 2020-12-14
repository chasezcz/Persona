'''
@File    :   jsonUtils.py
@Time    :   2020/12/14 16:55:04
@Author  :   Chengze Zhang 
@Contact :   chengze1996@gmail.com
@License :   Copyright (c) 2020 Chengze Zhang
'''

# here put the import lib

import json

def writeJson(filename, dic):
    with open(filename,'a', encoding="utf-8") as outfile:
        json.dump(dic,outfile,ensure_ascii=False)

def readJson(filename):
    with open(filename, "r", encoding="utf-8") as target:
        return json.load(target)