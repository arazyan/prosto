import pandas as pd

import funcs

exported_df = pd.read_excel('assets/exported.xlsx')
on_deal     = pd.read_excel('assets/ondeal.xlsx')


funcs.write_output(repr(exported_df.head())