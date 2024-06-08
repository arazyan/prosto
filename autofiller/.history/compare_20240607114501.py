import pandas as pd

exported_df = pd.read_excel('asseexported.xlsx')
on_deal     = pd.read_excel('ondeal.xlsx')

print(exported_df.head())