import pandas as pd
from sqlalchemy import create_engine

# File path to Kaggle dataset
path = '/Users/arpad/.cache/kagglehub/datasets/iamsouravbanerjee/customer-shopping-trends-dataset/versions/2/shopping_trends_updated.csv'
# load dataset
data = pd.read_csv(path)

# Extract, clean data, drop duplicates
customer_data = data[['Customer ID', 'Age', 'Gender', 'Frequency of Purchases']].drop_duplicates()

items_data = data[['Item Purchased', 'Category']].drop_duplicates().reset_index(drop=True)
items_data.insert(0, 'Item ID', range(1, len(items_data) + 1))

purchases_data = data[['Customer ID', 'Item Purchased', 'Purchase Amount (USD)', 'Discount Applied', 'Season']]
purchases_data = purchases_data.reset_index(drop=True)
purchases_data.insert(0, 'Purchase ID', range(1, len(purchases_data) + 1))

# Merge 'purchases_data' with 'items_data' to match Item IDs
purchases_data = purchases_data.merge(items_data, on='Item Purchased', how='inner')
purchases_data = purchases_data[
    ['Purchase ID', 'Customer ID', 'Item ID', 'Purchase Amount (USD)', 'Discount Applied', 'Season']
]

#Connect to the database
engine = create_engine('mysql+pymysql://arpad:NewStr0ngP%40ssword!@localhost/customer_segmentation')

# Upload the dataframes into the database
customer_data.to_sql('customer_data', con=engine, if_exists='replace', index=False)
items_data.to_sql('items_data', con=engine, if_exists='replace', index=False)
purchases_data.to_sql('purchases_data', con=engine, if_exists='replace', index=False)

engine.dispose()
print("Data successfully uploaded to MySQL database!")