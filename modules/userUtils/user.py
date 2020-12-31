'''
@File    :   User.py
@Time    :   2020/12/30 20:44:25
@Author  :   Chengze Zhang 
@Contact :   chengze1996@gmail.com
@License :   Copyright (c) 2020 Chengze Zhang
'''

# here put the import lib
import datetime
import json
import pandas as pd 

USER_TABLE_LABELS = [
    "userId",
    "name",
    "institutionId",
    "urls",
    "ips",
    "startTimes",
    "aveageContinueTime",
    "aveageHETime",
    "heNumber"
]

class User(object):
    """
    emmmmmmmmmmmmmmmmm
    """
    def __init__(self, sessionDF):
        """
        docstring
        """
        # 基础信息
        self.userId = sessionDF.userId.values[0]
        self.name = sessionDF.name.values[0]
        self.institutionId = sessionDF.institutionId.values[0]
        
        # URL 统计
        self.urls = dict(sessionDF.urls.value_counts().apply(str)) 
        # IP 历史
        self.ips = {}
        for ips, count in sessionDF.ips.value_counts().items():
            sessionIP = "127.0.0.1"
            for ip in ips.split("-"):
                if ip.startswith("127.") or ip.startswith("192."):
                    continue
                sessionIP = ip
            
            self.ips[sessionIP] = self.ips[sessionIP] + count if sessionIP in self.ips else count

        # 上线时间段
        self.startTimes = dict(sessionDF.startTime.apply(lambda x: datetime.datetime.fromtimestamp(x).hour).value_counts().apply(str))
        # 操作持续时间
        self.aveageContinueTime = (sessionDF.endTime - sessionDF.startTime).apply('mean')
        # 日志产生的平均间隔时间
        self.aveageHETime = sessionDF.aveageHETime.apply('mean')
        # 平均一次登陆产生的日志
        self.heNumber = sessionDF.heNumber.apply('mean')

    def getSet(self):
        return [
            str(self.userId),
            str(self.name),
            str(self.institutionId),
            json.dumps(self.urls),
            json.dumps(self.ips),
            json.dumps(self.startTimes),
            self.aveageContinueTime,
            self.aveageHETime,
            self.heNumber]