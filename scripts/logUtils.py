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
import pymysql
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
        self.statusCode = content[12]
        self.parameterType = content[13]
        self.parameterName = content[14]
        
        
        # select log version
        if content[len(content) - 1].isalnum():
            # last pos is port
            parameterValueEnd = len(content) - 5
            self.vpnip = 0
        else:
            # last pos is vpn ip
            self.vpnip = content[-1]
            parameterValueEnd = len(content) - 6
        self.parameterValue = " ".join(content[15:parameterValueEnd+1])
        self.header = content[parameterValueEnd+1]
        self.name = content[parameterValueEnd+2]
        self.ip = content[parameterValueEnd+3]
        self.port = content[parameterValueEnd+4]

    def simplyPrint(self):
        """
        supply a method to print all value.
        """
        # return "{0},{1},{2},{3},{4},{5},{6},{7},{8}\n".format(

        # # return "{0},{1}-{2},{3},{4},{5}:{6}\n".format(
        #     # self.date.strftime('%Y-%m-%d %H:%M:%S.%f'),
        #     self.timestamp,
        #     self.userId,
        #     self.name,
        #     self.url,
        #     self.parameterName,
        #     self.parameterValue,
        #     self.header,
        #     self.ip,
        #     self.port)


        return "{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14}".format(

        # return "{0},{1}-{2},{3},{4},{5}:{6}\n".format(
            # self.date.strftime('%Y-%m-%d %H:%M:%S.%f'),
            self.timestamp,
            self.threadId,
            self.institutionId,
            self.userId,
            self.url,
            self.method,
            self.method,
            self.statusCode,
            self.parameterType,
            self.parameterName,
            self.parameterValue,
            self.header,
            self.ip,
            self.port,
            self.vpnip
            )


def argumentParser():
    """ 
    Get argument parser.
    """    
    parser = argparse.ArgumentParser(usage="it's usage tip.", description="help info.")
    parser.add_argument("--input", help="where the origin data.", dest="inputDataPath")
    parser.add_argument("--output", help="where the dataset output.", dest="outputDataPath")
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
            if ".log" in f:
                allfiles.append(os.path.join(root, f))
    return allfiles

def connectDB(parameter_list):
    """
    Connect to the database and create the table, returning the database handle.
    """
    
    db = pymysql.connect('localhost', 'persona', 'Mr.Zhang123', 'persona')

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    
    # 使用 execute() 方法执行 SQL，如果表存在则删除
    cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")
    
    # 使用预处理语句创建表
    sql = """CREATE TABLE EMPLOYEE (
            FIRST_NAME  CHAR(20) NOT NULL,
            LAST_NAME  CHAR(20),
            AGE INT,  
            SEX CHAR(1),
            INCOME FLOAT )"""
    
    cursor.execute(sql)
    
    return db

    

if __name__ == '__main__':
    config = argumentParser()
    # get all files.
    files = getFilesByPath(config.inputDataPath)
    if not files: 
        print("there no any file. recorrect the input path.")
        os._exit(0)
    # wr = open("data/tmp.csv", "w")

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
                    print(he.simplyPrint())
                    # wr.write(he.simplyPrint)
                except Exception as e:
                    pass