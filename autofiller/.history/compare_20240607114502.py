import pandas as pd

exported_df = pd.read_excel('assets/exported.xlsx')
on_deal     = pd.read_excel('ondeal.xlsx')

print(exported_df.head())