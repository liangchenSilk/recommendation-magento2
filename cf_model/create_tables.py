# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 16:24:09 2019
@author: Silk
"""
import db_info
import pymysql

myhost = db_info.config['host']
myuser = db_info.config['user']
mypassword = db_info.config['password']
mydb = db_info.config['database']
myport = db_info.config['port']

db = pymysql.connect(host=myhost,user=myuser,password=mypassword,db=mydb,port=myport)

cursor = db.cursor()

try:
    #create table schema
    cursor.execute("DROP TABLE IF EXISTS rec_user_product_count")
    sql = """CREATE TABLE rec_user_product_count (
            id INT(11) auto_increment primary key NOT NULL,
            customer_id INT(11) NOT NULL,
            product_id INT(11) NOT NULL,
            count INT (11))"""
    cursor.execute(sql)
    print("table 'count' create success")
    
    #create table product mapping
    cursor.execute("DROP TABLE IF EXISTS rec_index_product_mapping")
    sql = """CREATE TABLE rec_index_product_mapping (
            id INT(11) auto_increment primary key NOT NULL,
            product_id INT(11) NOT NULL)"""
    cursor.execute(sql)
    print("table 'product mapping' create success")
    
    #create table customer mapping
    cursor.execute("DROP TABLE IF EXISTS rec_index_customer_mapping")
    sql = """CREATE TABLE rec_index_customer_mapping (
            id INT(11) auto_increment primary key NOT NULL,
            customer_id INT(11) NOT NULL)"""
    cursor.execute(sql)
    print("table 'customer mapping' create success")
    
    #create recommend customer-product table, real product id and customer id
    cursor.execute("DROP TABLE IF EXISTS rec_result")
    sql = """CREATE TABLE rec_result (
            id INT(11) auto_increment primary key NOT NULL,
            customer_id INT(11) NOT NULL,
            product_id INT(11) NOT NULL)"""
    cursor.execute(sql)
    print("table 'recommendation result table' create success")
    
    
    #create table category mapping
    cursor.execute("DROP TABLE IF EXISTS rec_index_category_mapping")
    sql = """CREATE TABLE rec_index_category_mapping (
            id INT(11) auto_increment primary key NOT NULL,
            category_id INT(11) NOT NULL)"""
    cursor.execute(sql)
    print("table 'category mapping' create success")
    
    
    #create table featured product category
    cursor.execute("DROP TABLE IF EXISTS rec_product_category")
    sql = """CREATE TABLE rec_product_category (
            id INT(11) auto_increment primary key NOT NULL,
            product_id INT(11) NOT NULL,
            category_id INT(11) NOT NULL)"""
    cursor.execute(sql) 
    print("table 'pro cat attribute' create success")
    
    sql = """CREATE TABLE rec_product2product_distance (
            id INT(11) auto_increment primary key NOT NULL,
            orig_product_id INT(11) NOT NULL,
            recomm_product_id INT(11) NOT NULL,
            distance DECIMAL(20, 18) Default 0)"""
    cursor.execute(sql)
    print("table 'count' create success")
    
    db.commit() 
except Exception as e:
    print(str(e))
    
db.close()

