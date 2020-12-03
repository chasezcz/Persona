'''
@File    :   mysql.py
@Time    :   2020/12/02 13:14:20
@Author  :   Chengze Zhang 
@Contact :   chengze1996@gmail.com
@License :   Copyright (c) 2020 Chengze Zhang
'''

# here put the import lib
import pymysql

def connectDB(parameter_list):
    """
    Connect to the database and create the table, returning the database handle.
    """
    
    db = pymysql.connect('localhost', 'persona', 'Mr.Zhang123', 'persona')

    # create a cursor object by method cursor()
    cursor = db.cursor()
    
    # use execute(), delete table if it exists.
    cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")
    # create table.
    sql = """CREATE TABLE EMPLOYEE (
            FIRST_NAME  CHAR(20) NOT NULL,
            LAST_NAME  CHAR(20),
            AGE INT,  
            SEX CHAR(1),
            INCOME FLOAT )"""
    
    cursor.execute(sql)
    
    return db
