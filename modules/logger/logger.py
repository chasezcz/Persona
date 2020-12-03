'''
@File    :   logger.py
@Time    :   2020/12/02 14:50:35
@Author  :   Chengze Zhang 
@Contact :   chengze1996@gmail.com
@License :   Copyright (c) 2020 Chengze Zhang
'''

# here put the import lib
import logging
import os
import sys

def init(level=logging.DEBUG):

    logging.basicConfig(
        format='%(asctime)s [%(levelname)s]: %(message)s',
        datefmt='%Y-%m-%d %I:%M:%S',
        level=level)

log = logging.getLogger("inf")

if __name__ == "__main__":
    init()
    log = logging.getLogger("inf")
    log.info("fjewif")