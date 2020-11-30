'''
@File    :   logUtils.py
@Time    :   2020/11/30 14:34:55
@Author  :   Chengze Zhang 
@Contact :   chengze1996@gmail.com
@License :   Copyright (c) 2020 Chengze Zhang
@Desc    :   Copy from chasezcz/LogAnalyse/logUtils/httpEvent.py, create a class which descript the log struct.
'''

# here put the import lib


import os
import datetime
import argparse
from collections import defaultdict

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
            content.append(s.replace(",", " "))

        # remove ERROR log and abnormal log
        if content[2] == "ERROR" or len(content) < 14:
            raise Exception("error log")

        try:
            tmpDate = "{0} {1}".format(content[0], content[1])
            # parse date string to datetime
            self.timestamp = datetime.datetime.strptime(
                tmpDate, '%Y-%m-%d %H:%M:%S %f').timestamp()
        except Exception as identifier:
            raise Exception(identifier)
        

        self.threadId = content[7]
        self.institutionId = content[8]
        self.userId = content[9]
        self.url = content[10]
        self.method = content[11]

        # parameters
        if content[len(content) - 1].isalnum():
            self.port = content[len(content) - 1]
            self.ip = content[len(content) - 2]
            self.name = content[len(content) - 3]
            self.header = content[len(content) - 4]

            self.parameter = content[14]
            self.parameterValue = " ".join(content[i]
                                          for i in range(15, len(content)-4))

        else:
            self.port = "0"
            self.ip = content[len(content) - 1]
            self.name = content[len(content) - 2]
            self.header = content[len(content) - 3].replace(" ", ",")
            self.parameter = content[14]
            self.parameterValue = " ".join(content[i]
                                          for i in range(15, len(content)-3))
        


    def simplyPrint(self):
        """
        supply a method to print all value.
        """
        return "{0},{1},{2},{3},{4},{5},{6},{7},{8}\n".format(

        # return "{0},{1}-{2},{3},{4},{5}:{6}\n".format(
            # self.date.strftime('%Y-%m-%d %H:%M:%S.%f'),
            self.timestamp,
            self.userId,
            self.name,
            self.url,
            self.parameter,
            self.parameterValue,
            self.header,
            self.ip,
            self.port)



def argumentParser():
    """ 
    Get argument parser.
    """    
    parser = argparse.ArgumentParser(usage="it's usage tip.", description="help info.")
    parser.add_argument("--input", help="where the origin data.", dest="inputDataPath")
    
    args = parser.parse_args()
    return args

def getFilesByPath(path):
    """
    Gets all files under the specified path
    :param path: specific path
    :return: absolute path list for all files
    """
    allfiles = list()
    for root, _, files in os.walk(path):
        for f in files:
            allfiles.append(os.path.join(root, f))
    return allfiles


if __name__ == '__main__':
    config = argumentParser()
    # get all files.
    files = getFilesByPath(config.inputDataPath)
    if not files: 
        print("there no any file. recorrect the input path.")
        os._exit(0)

    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            # read raw log by line.
            for line in f:
                try:
                    he = HttpEvent(line)
                    # if he.length not in leng:
                    #     leng[he.length] = 0
                    # leng[he.length] += 1
                    # he.simplyPrint()

                except Exception as e:
                    pass
