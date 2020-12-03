'''
@File    :   argumentParser.py
@Time    :   2020/12/02 14:56:54
@Author  :   Chengze Zhang 
@Contact :   chengze1996@gmail.com
@License :   Copyright (c) 2020 Chengze Zhang
'''

# here put the import lib
import argparse

def argumentParser():
    """ 
    Get argument parser.
    """    
    parser = argparse.ArgumentParser(usage="it's usage tip.", description="help info.")
    parser.add_argument("--input", help="where the origin data.", dest="inputDataPath", default="data/origin")
    parser.add_argument("--output", help="where the dataset output.", dest="outputDataPath", default="data/tmp")
    args = parser.parse_args()
    return args