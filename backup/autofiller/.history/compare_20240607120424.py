import pandas as pd

import funcs

exported_df = pd.read_excel('assets/exported.xlsx')
on_deal     = pd.read_excel('assets/ondeal.xlsx')

df = exported_df['ФИО']
funcs.write_df('output.xlsx', exported_df['ФИО'])
