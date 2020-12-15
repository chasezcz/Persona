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
from modules.logUtils.httpEvent import HttpEvent, HE_TABLE_LABELS
from modules.logUtils.session import Session, SESSION_TABLE_LABELS
from modules.logUtils.urlFilter import urlConvert
from modules.fileUtils.jsonUtils import writeJson, readJson
from modules.fileUtils.fileUtils import getFilesByPath
from modules.config.argumentParser import argumentParser
from modules.config.configParser import getValue as getValueFromConfig

# CONFIG
LOG_LEVEL = log.INFO

def collectLogs(input=getValueFromConfig("input"), baseDataSet="data/tmp/full.csv", randomSample=False)-> (pd.DataFrame, dict):
    """
    Run the collector to structurally extract all the log files in "RAW_DATA_PATH"
    """
    
    # get all files.
    files = getFilesByPath(input)
    if not files: 
        log.error("there no any file. recorrect the input path.")
        return None, None, None
    
    # IF SMIPLY WRITE TO CSV
    # with open(os.path.join(output, "", "tmp.csv"), "w", encoding="utf-8") as target:
    #     target.write(TABLE_LABELS+'\n')
    # END

    # DEV MODE
    if randomSample:
        import random
        files = random.sample(files, 20)
        log.info("get number of files is {0}".format(len(files)))
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
        df = pd.DataFrame(data = data, columns = HE_TABLE_LABELS)
        del data

        # delete log which is bugs
        df = df.drop(index=(df.loc[(df.name=='何群辉')].index))
        # delete unused log
        df = df.drop(index=(df.loc[(df.headers=="null")].index))
        # delete unused column
        df = df.drop(['threadId', 'statusCode', 'parameterType'], axis=1)

        # convert all urls
        df.url = df.url.apply(urlConvert, args=(set(df.userId.values), set(df.institutionId.values),  set(df.name.values),))
        
        # save to CSV
        df.to_csv(baseDataSet, sep=getValueFromConfig("sep"))

        # get url index map
        urlSet = set(df.url.values)
        urlToIndex = {url:i.__str__() for i, url in enumerate(urlSet)}
        urlIndexToUrl = {i.__str__():url for i, url in enumerate(urlSet)}
        log.info("url count: {0}".format(len(urlSet)))
        if not os.path.exists('data/url'):
            os.makedirs('data/url')

        writeJson("data/url/urlToIndex.json", urlToIndex)
        writeJson("data/url/urlIndexToUrl.json", urlIndexToUrl)

        return df, urlToIndex, urlIndexToUrl
    else:
        df = pd.read_csv(baseDataSet, sep=getValueFromConfig("sep"), index_col=[0])
        return df, readJson("data/url/urlToIndex.json"), readJson("data/url/urlIndexToUrl.json")

def combineSessions(baseDF, urlToIndex, ipLocation)->pd.DataFrame:
    """
    Identify the internal session and generate the SessionID based on the previously generated baseDataset;
    """
    threshold = getValueFromConfig("sessionThreshold")
    sessions = []
    
    for userId, indexs in baseDF.groupby('userId').groups.items():
        log.debug("cur combine session of {0}".format(userId))
        tmpSessions = Session.generateSession(baseDF.loc[indexs].copy(), urlToIndex, threshold, ipLocation)
        sessions.extend(tmpSessions)
    
    sessionDF = pd.DataFrame(data=sessions, columns=SESSION_TABLE_LABELS)
    
    return sessionDF

def combineUserBySession(sessionDF: pd.DataFrame):
    """
    docstring
    """
    # delete unused column
    userDF = sessionDF.drop(['urls', "startTime", "endTime"], axis=1)

    def combine(x):
        p = set(x.tolist())
        return ','.join(p)

    userDF = userDF.groupby(by=['userId']).agg({
        'name': [combine],
        'aveageHETime': ['mean'],
        'ips': [combine],
        'citys': [combine]
    })
    return userDF

if __name__ == "__main__":
    logInit(LOG_LEVEL)
    args = argumentParser()
    pd.set_option('display.float_format', lambda x: '%.3f' % x)

    baseDF, urlToIndex, urlIndexToUrl = collectLogs(args.inputDataPath, args.baseDataSet, args.randomSample)
    
    sessionDF = combineSessions(baseDF, urlToIndex, args.iplocation)
    del(baseDF)
    log.debug("SESSION DATAFRAME")
    log.debug(sessionDF)

    userDF = combineUserBySession(sessionDF)
    log.debug("USER DATAFRAME")
    log.debug(userDF)
    log.info(userDF.filter([('name', 'combine'), ('citys', 'combine')])[:20])
    log.info(userDF[userDF['name']['combine']=='石小文'])

