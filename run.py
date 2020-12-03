'''
@File    :   run.py
@Time    :   2020/12/02 14:49:11
@Author  :   Chengze Zhang 
@Contact :   chengze1996@gmail.com
@License :   Copyright (c) 2020 Chengze Zhang
'''

# here put the import lib
import os

import logging as log
import pandas as pd

from modules.logger.logger import init as logInit
from modules.logUtils.httpEvent import HttpEvent, TABLE_LABELS
from modules.fileUtils.fileUtils import getFilesByPath
from modules.config.argumentParser import argumentParser
from modules.config.configParser import getValue as getValueFromConfig

# CONFIG
LOG_LEVEL = log.DEBUG

def combine(input=getValueFromConfig("input"), output=getValueFromConfig("output")):
    """
    Run the collector to structurally extract all the log files in "RAW_DATA_PATH"
    """
    
    # get all files.
    files = getFilesByPath(input)
    if not files: 
        print("there no any file. recorrect the input path.")
        return
    
    # IF SMIPLY WRITE TO CSV
    # with open(os.path.join(output, "", "tmp.csv"), "w", encoding="utf-8") as target:
    #     target.write(TABLE_LABELS+'\n')
    # END

    data = []
    for file in files:
        count = 0
        with open(file, 'r', encoding='utf-8') as f:
            # read raw log by line.
            for line in f:
                try:
                    he = HttpEvent(line)
                    count += 1
                    # append to Data
                    data.extend([he.getSet()])
                except Exception as e:
                    log.debug(e)
        log.info("{0} write {1} lines".format(file, count))
    
    # convert List to DataFrame
    df = pd.DataFrame(data = data, columns = TABLE_LABELS)
    urlDF = df.url
    urlsCount = urlDF.value_counts()
    
    


if '__name__' == '__main__':

    args = argumentParser()
    logInit(LOG_LEVEL)
    combine(args.inputDataPath, args.outputDataPath)

