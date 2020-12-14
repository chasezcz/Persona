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
from modules.logUtils.urlFilter import urlConvert
from modules.fileUtils.fileUtils import getFilesByPath
from modules.config.argumentParser import argumentParser
from modules.config.configParser import getValue as getValueFromConfig

# CONFIG
LOG_LEVEL = log.DEBUG

def collectLogs(input=getValueFromConfig("input"), baseDataSet="data/tmp/full.csv"):
    """
    Run the collector to structurally extract all the log files in "RAW_DATA_PATH"
    """
    
    # get all files.
    files = getFilesByPath(input)
    if not files: 
        print("there no any file. recorrect the input path.")
        return None
    
    # IF SMIPLY WRITE TO CSV
    # with open(os.path.join(output, "", "tmp.csv"), "w", encoding="utf-8") as target:
    #     target.write(TABLE_LABELS+'\n')
    # END

    if (not os.path.exists(baseDataSet)) or (os.path.exists(baseDataSet) and getValueFromConfig("reGenerateBaseDataSet")):
        data = []
        for file in files:
            count = 0
            with open(file, 'r', encoding='utf-8') as f:
                # read raw log by line.
                for line in f:
                    try:
                        he = HttpEvent(line)

                        # filter url which userId is 'null'
                        if he.userId == 'null': continue

                        # append to Data
                        data.extend([he.getSet()])
                        count += 1
                    except Exception as e:
                        log.debug(e)
            log.info("{0} write {1} lines".format(file, count))
        
        # convert List to DataFrame
        df = pd.DataFrame(data = data, columns = TABLE_LABELS)
        del data

        # delete log which is bugs
        df = df.drop(index=(df.loc[(df.name=='何群辉')].index))
        # delete unused log
        df = df.drop(index=(df.loc[(df.header=="null")].index))
        # delete unused column
        df = df.drop(['threadId', 'statusCode', 'parameterType'], axis=1)

        # convert all urls
        df['url'] = df['url'].apply(urlConvert, args=(set(df.userId.values), set(df.institutionId.values),  set(df.name.values),))
        
        # Sort by userId primary key, with time as the secondary key
        df.sort_values(by=['userId', 'timestamp'])

        # save to CSV
        df.to_csv(baseDataSet, sep=getValueFromConfig("sep"))
        return df
    else:
        df = pd.read_csv(baseDataSet, sep=getValueFromConfig("sep"))
        return df

def combineSessions(baseDF):
    """
    There are three tasks: 
        1. identify the internal session and generate the SessionID based on the previously generated baseDataset;
        2. Convert url to ID to generate the mapping table of URL to urlIdx;
        3. Generate URL jump sequence table.
    """
    return 1


if '__name__' == '__main__':

    args = argumentParser()
    logInit(LOG_LEVEL)
    
    baseDF = collectLogs(args.inputDataPath, args.baseDataSet)

    finalDF = combineSessions(baseDF)
    print(baseDF.shape, finalDF.shape)
