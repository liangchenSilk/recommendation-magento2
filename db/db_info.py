# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 16:25:03 2019

@author: Silk
"""

config = {
        'host' : '127.0.0.1',
        'user' : 'magento',
        'password' : '12345abc',
        'port' : 3306,
        'database' : 'mor'
}

'''
#test connection
import db_info
import pymysql

myhost = db_info.config['host']
myuser = db_info.config['user']
mypassword = db_info.config['password']
mydb = db_info.config['database']
myport = db_info.config['port']

db = pymysql.connect(host=myhost,user=myuser,password=mypassword,db=mydb,port=myport)
cursor = db.cursor()
sql = "select * from admin_user"
cursor.execute(sql)
res = cursor.fetchall()
print(len(res))
for row in res:
    print(row[0])
'''