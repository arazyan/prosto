import pandas as pd
import funcs

exported_df = pd.read_excel('assets/exported.xlsx')
on_deal     = pd.read_excel('assets/ondeal.xlsx')

temp_df = exported_df.iloc[:,1]

funcs.write_df('output.xlsx', temp_df)

