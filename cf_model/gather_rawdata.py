# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 16:52:15 2019

@author: Silk
"""

import db_info
import pymysql

class GatherRawData():
    def __init__(self):
        myhost = db_info.config['host']
        myuser = db_info.config['user']
        mypassword = db_info.config['password']
        mydb = db_info.config['database']
        myport = db_info.config['port']
        self.db = pymysql.connect(host=myhost,user=myuser,password=mypassword,db=mydb,port=myport)
        self.cursor = self.db.cursor()

    def pickDataRange(self, start, end):
        
        #fetch queries
        sqlFetchOrder = """select a.customer_id, a.entity_id, b.order_id, b.product_id, b.sku, b.qty_ordered 
                from sales_order as a inner join sales_order_item as b on a.entity_id = b.order_id 
                where a.customer_id is not null 
                and a.created_at >= %s
                and a.created_at < %s 
                order by a.customer_id"""
        
        sqlFetchViewRecord = """select a.customer_id, a.product_id, count(product_id)
                        from report_viewed_product_index as a 
                        group by a.customer_id, a.product_id
                        having a.customer_id is not NULL"""
        
              
        sqlFetchPro2Cat = """SELECT category_id, product_id FROM catalog_category_product
                        WHERE product_id IN 
                        (SELECT product_id FROM rec_product_index_mapping)"""
        
        #truncate queries
        sqlClearCount = "TRUNCATE TABLE rec_user_product_count"
        sqlClearProductMapping = "TRUNCATE TABLE rec_product_index_mapping"
        sqlClearCustomerMapping = "TRUNCATE TABLE rec_customer_index_mapping"
        sqlClearCategoryMapping = "TRUNCATE TABLE rec_category_index_mapping"
        sqlClearPro2Cat = "TRUNCATE TABLE rec_product_category"
        
        #insert processed data
        sqlInsertUserProductCount = "INSERT INTO rec_user_product_count (customer_id, product_id, count) VALUES (%s, %s, %s)"        
        sqlProductIndexMapping = "INSERT INTO rec_product_index_mapping (product_id) values (%s)"
        sqlCustomerIndexMapping = "INSERT INTO rec_customer_index_mapping (customer_id) values (%s)"
        sqlCategoryIndexMapping = "INSERT INTO rec_category_index_mapping (category_id) values (%s)"
        sqlInsertProCat = "INSERT INTO rec_product_category (product_id, category_id) values (%s, %s)"
        
        count = {}
        proCat = {}
        product_set = set()
        customer_set = set()
        category_set = set()
        
        try:
            print("start with empty tables")
            # start with fresh data range
            self.cursor.execute(sqlClearCount)
            self.cursor.execute(sqlClearProductMapping)
            self.cursor.execute(sqlClearCustomerMapping)
            self.cursor.execute(sqlClearCategoryMapping)
            self.cursor.execute(sqlClearPro2Cat)
            
            #fetch order data: prod, customer, count
            print("collect order data")
            self.cursor.execute(sqlFetchOrder, [start, end])
            results = self.cursor.fetchall()
            line = 0
            for row in results:
                line = line + 1
                customer_id = row[0]
                product_id = row[3]
                qty = row[5]
                
                product_set.add(product_id)
                customer_set.add(customer_id)
                
                if customer_id in count:
                    count[customer_id][product_id] = count[customer_id].get(product_id, 0) + qty
                else:
                    count[customer_id] = {}
                    count[customer_id][product_id] = qty
                #print(line)
            print("fetch order success...Total of {} lines".format(line))
            
            #fetch viewed data: product, customer, count
            print("collect view history...")
            self.cursor.execute(sqlFetchViewRecord)
            results = self.cursor.fetchall()
            line = 0
            for row in results:
                line = line + 1
                customer_id = row[0]
                product_id = row[1]
                qty = row[2]
                
                product_set.add(product_id)
                customer_set.add(customer_id)
                
                if customer_id in count:
                    count[customer_id][product_id] = count[customer_id].get(product_id, 0) + qty
                else:
                    count[customer_id] = {}
                    count[customer_id][product_id] = qty
                #print(line)
            print("fetch view history success...Total of {} lines".format(line))
                 
            
            #update to count table
            for customer in count:
                for product, product_count in count[customer].items():
                    params = [customer, product, product_count]
                    #print(params)
                    self.cursor.execute(sqlInsertUserProductCount, params)
            print("update count table success")
            
            #update product index mapping     
            for product_id in product_set:
                self.cursor.execute(sqlProductIndexMapping, [product_id])
            print("update product mapping table success")
            
            #update customer index mapping 
            for customer_id in customer_set:
                self.cursor.execute(sqlCustomerIndexMapping, [customer_id])
            print("update customer mapping table success")          
            
            #fetch product category
            self.cursor.execute(sqlFetchPro2Cat)
            results = self.cursor.fetchall()
            for row in results:
                cat = row[0]
                pro= row[1]
                if pro in proCat:
                    if cat not in proCat[pro]:
                        proCat[pro].append(cat)
                else:
                    proCat[pro] = []
                    proCat[pro].append(cat)
                category_set.add(cat)
                
            #update pro category table
            for pro in proCat:
                for cat in proCat[pro]:
                    self.cursor.execute(sqlInsertProCat, [pro, cat])
            print("update product category table success")
            
            #update category index mapping
            for category_id in category_set:
                self.cursor.execute(sqlCategoryIndexMapping, [category_id])
            print("update category mapping table success")
            
            print("all update complete...")
            self.db.commit()
            
        except Exception as e:
            print("failed to update data")
            print(str(e))
            self.db.rollback()
