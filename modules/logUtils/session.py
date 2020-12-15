'''
@File    :   session.py
@Time    :   2020/12/14 17:31:47
@Author  :   Chengze Zhang 
@Contact :   chengze1996@gmail.com
@License :   Copyright (c) 2020 Chengze Zhang
'''

# here put the import lib
import json
import pandas as pd
import logging as log
from modules.api.iplocation import getCitysByIPs

SESSION_TABLE_LABELS = [
    "userId",
    "name",
    "institutionId",
    "urls",
    "ips",
    "startTime",
    "endTime",
    "aveageHETime",
    "heNumber",
    "citys"
]

class Session(object):
    """
    emmmmmmmmmmmmmmmmm
    """

    def __init__(self, hes, ipLocation: bool):
        """
        docstring
        """
        self.userId = hes[0].userId
        self.name = hes[0].name
        self.institutionId = hes[0].institutionId
        self.urls = []
        timestamps = []
        self.citys = set()
        self.ips = set()
        for he in hes:
            timestamps.append(he.timestamp)
            self.urls.append(he.url),
            self.ips.add(he.ip)

        # Units are seconds
        self.startTime = timestamps[0]
        self.endTime = timestamps[-1]
        if ipLocation:
            self.citys = getCitysByIPs(self.ips)
        self.heNumber = len(self.urls)

        self.aveageHETime = sum([timestamps[i]-timestamps[i-1] for i in range(1, len(timestamps))]) / self.heNumber
  
    def getSet(self):
        return [
            self.userId,
            self.name,
            self.institutionId,
            "-".join(self.urls),
            "-".join(self.ips),
            self.startTime,
            self.endTime,
            self.aveageHETime,
            self.heNumber,
            "-".join(self.citys)
        ]
        
    @staticmethod
    def generateSession(hes: pd.DataFrame, urlToIndex, threshold, ipLocation)->list:
        """
        Used to divide sessions into separate sessions in an unordered pile of logs.
        """
        #########################################################
        # TODO: simply save the index of url, ip, and drop others.
        #########################################################
        
        sessions = []
        
        # read by line
        paths = []
        lastHeaderKey, lastHEDate = "", 0
        
        # sort by timestamp
        hes = hes.sort_values(by='timestamp')
        hes.url = hes.url.apply(lambda x: urlToIndex[x])

        for he in hes.itertuples():
            #  get session key in headers
            headersJSON = json.loads(he.headers)
            flag = False
            for header in headersJSON:
                if header['value']==lastHeaderKey:
                    lastHeaderKey = header['value']
                    flag = True
            
            if not flag and float(he.timestamp) - lastHEDate > threshold:
                # start a new session
                if paths:
                    session = Session(paths, ipLocation)
                    sessions.append(session.getSet())
                    # sessions.append("-".join([urlToIndex[url] for url in paths]))
                paths.clear()
                lastHeaderKey = headersJSON[0]['value']
            
            # update paths 
            paths.append(he)
            lastHEDate = he.timestamp
        
        session = Session(paths, ipLocation)
        sessions.append(session.getSet())
        # sessions.append("-".join([urlToIndex[url] for url in paths]))
        return sessions