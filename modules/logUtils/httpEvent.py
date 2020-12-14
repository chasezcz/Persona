'''
@File    :   httpEvent.py
@Time    :   2020/12/02 12:52:40
@Author  :   Chengze Zhang 
@Contact :   chengze1996@gmail.com
@License :   Copyright (c) 2020 Chengze Zhang
'''

# here put the import lib
import datetime
from modules.config.configParser import getValue

class HttpEvent(object):
    """
    log struct
    """
    def __init__(self, originLog: str):
        """
        init httpEvent
        :param originLog: raw data
        :param saveOriginData: whether save raw data
        """
        splits = originLog.split(" ")
        content = list()

        for s in splits:
            s = s.strip()
            if s == "": continue
            # content.append(s)
            content.append(s)

        # remove ERROR log and abnormal log
        if content[2] == "ERROR" or len(content) < 14:
            raise Exception("error log")
        try:
            tmpDate = "{0} {1}".format(content[0], content[1])
            # parse date string to datetime
            self.timestamp = datetime.datetime.strptime(
                tmpDate, '%Y-%m-%d %H:%M:%S,%f').timestamp()
        except Exception as identifier:
            raise Exception(identifier)

        self.threadId = content[7]
        self.institutionId = content[8]
        self.userId = content[9]
        self.url = content[10]
        self.method = content[11]
        self.statusCode = content[12]
        self.parameterType = content[13]
        self.parameterName = content[14]
        
        
        # select log version
        if "." in content[-1] and isNumber(content[-2]):
            # last pos is vpn ip

            self.vpnip = content[-1]
            self.port = content[-2]
            parameterValueEnd = len(content) - 6
        elif "." in content[-1]:
            # last pos is ip

            self.vpnip = "0"
            self.port = "0"
            parameterValueEnd = len(content) - 4
        else:
            # last pos is port

            self.vpnip = "0"   
            self.port = content[-1]
            parameterValueEnd = len(content) - 5
           
        self.parameterValue = " ".join(content[15:parameterValueEnd+1])
        self.header = content[parameterValueEnd+1]
        self.name = content[parameterValueEnd+2]
        self.ip = content[parameterValueEnd+3]

    def simplyPrint(self):
        """
        supply a method to print all value.
        """
        sep = getValue("sep")
        return sep.join([
            str(self.timestamp),
            self.threadId,
            self.institutionId,
            self.userId,
            self.url,
            self.method,
            self.statusCode,
            self.parameterType,
            self.parameterName,
            self.parameterValue.replace(sep, ""),
            self.header,
            self.name,
            self.ip,
            self.port,
            self.vpnip
        ])
        
    def getSet(self):
        """
        Gets all valid data for the current instance in sequence.
        """
        sep = getValue("sep")
        return [
            str(self.timestamp),
            self.threadId,
            self.institutionId,
            self.userId,
            self.url,
            self.method,
            self.statusCode,
            self.parameterType,
            self.parameterName,
            self.parameterValue.replace(sep, ""),
            self.header,
            self.name,
            self.ip,
            self.port,
            self.vpnip
        ]


TABLE_LABELS = [
    "timestamp",
    "threadId",
    "institutionId",
    "userId",
    "url",
    "method",
    "statusCode",
    "parameterType",
    "parameterName",
    "parameterValue",
    "header",
    "name",
    "ip",
    "port",
    "vpnip"
]

def isNumber(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False