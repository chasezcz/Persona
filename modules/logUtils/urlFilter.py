'''
@File    :   urlFilter.py
@Time    :   2020/12/03 15:49:32
@Author  :   Chengze Zhang 
@Contact :   chengze1996@gmail.com
@License :   Copyright (c) 2020 Chengze Zhang
'''

# here put the import lib

class UrlFilter(object):
    """
    For statistics-based URL filters.
    """
    def __init__(self):
        self.set = dict()
        self.subUrlSet = dict()
        