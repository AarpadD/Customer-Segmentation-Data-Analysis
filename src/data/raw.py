import kagglehub
import pandas as pd
import os

# Download latest version
path = kagglehub.dataset_download("iamsouravbanerjee/customer-shopping-trends-dataset")
print("Path to dataset files:", path)

data_path = "/Users/arpad/.cache/kagglehub/datasets/iamsouravbanerjee/customer-shopping-trends-dataset/versions/2"
#files = os.listdir(data_path)
#print("Files in dataset: ", files)
test_data = pd.read_csv(os.path.join(data_path, 'shopping_trends_updated.csv'))

print("First few rows of test_dataset:")
print(test_data.head())
