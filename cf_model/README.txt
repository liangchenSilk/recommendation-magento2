Manual:
1. run create_tables.py
2. run build.py to process magento data and export to train txt data file
3. Move trainY, trainR, trainX to ML folder for modeling
4. Move pred.txt. prodX.txt back.
5. run predic to calculate prod2prod distance and write to db

database tables:

1. rec_user_product_count
Record product-user matrix for collabrative filtering (Matrix Y)
magento_product_id vs magento_user_id

2. rec_product_category
Record product-category (feature) matrix (Matrix X)
magento_product_id vs magento_category_id

3. rec_index_product_mapping
Record the magento product_id to training index

4. rec_index_customer_mapping
Record the magento customer_id to training index

5. rec_index_category_mapping
Record the magento category_id to training index

6. rec_product2product_distance
product to product distance (X2X distance after training)
magento_product_id vs magento_product_id

4. rec_result
record recommended product series to customers (magento_customer_id - magento_product_id)

*db_info.py
database credentials

*create_tables.py
Create usable tables

*gather_rawdata.py
process magento data and import to staging tables.
Magento data: user ordered items, user viewed items.
method: pickDataRange(d1, d2) to update database.
After processing: user product count, product2category (feature).

*data.py
Data class.
1. getCountData: extract from 'rec_user_product_count'. Return training Y matrix, and R matrix in converted model index.
2. getViewedData: return product to user viewed data
3. storeProd2ProdDist: import the product2product distance to db.

*build.py
Export txt file for ML model training data

*predic.py
Export data to db after calculate the prod2prod distance






