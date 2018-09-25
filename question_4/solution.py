import pandas as pd
import os

data = pd.read_excel('PYTHON_SAMPLE_FILE.xlsx')
non_duplicate_data = data.drop_duplicates()

#print all non duplcate values
print non_duplicate_data.values

#print length of non duplicate values
print non_duplicate_data.shape[0]
