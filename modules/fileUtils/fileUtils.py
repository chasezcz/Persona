'''
@File    :   fileUtils.py
@Time    :   2020/12/02 15:14:09
@Author  :   Chengze Zhang 
@Contact :   chengze1996@gmail.com
@License :   Copyright (c) 2020 Chengze Zhang
'''

# here put the import lib
import os 

def getFilesByPath(path):
    """
    Gets all files under the specified path
    :param path: specific path
    :return: absolute path list for all files
    """
    allfiles = list()
    for root, _, files in os.walk(path):
        for f in files:
            if ".log" in f:
                allfiles.append(os.path.join(root, f))
    return allfiles