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
    parser.add_argument("--baseDataSet", help="where the dataset output.", dest="baseDataSet", default="data/tmp")
    parser.add_argument("--reGenerateBaseDataSet", help="rebuild baseDataSet", dest="reGenerateBaseDataSet", default=False)
    args = parser.parse_args()
    

    
    return args