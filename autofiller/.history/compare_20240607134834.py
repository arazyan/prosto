import pandas as pd

import funcs

exported_df = pd.read_excel('assets/exported.xlsx')
on_deal     = pd.read_excel('assets/ondeal.xlsx')

exp_df = exported_df['ФИО'].drop_duplicates()
on_deal_list = on_deal.to_string(index=False).split('\n')


for i in range(len(on_deal_list)):
    on_deal_list[i] = [elem for elem in on_deal_list[i].split(' ') if elem != '' and elem not in ('0')]
    on_deal_list[i] = [' '.join(on_deal_list[i])]
    
temp_df = pd.DataFrame(on_deal_list)
#print(on_deal_list)
funcs.write_df('output.xlsx', temp_df)
