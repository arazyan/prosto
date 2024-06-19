import pandas as pd

import funcs



exp_df = exported_df['ФИО'].drop_duplicates()
on_deal_list = on_deal.to_string(index=False).split('\n')


for i in range(len(on_deal_list)):
    on_deal_list[i] = [elem for elem in on_deal_list[i].split(' ') if elem != '' and elem not in (str(x) for x in range(0, 10))]
    on_deal_list[i] = [' '.join(on_deal_list[i])]
    
temp_df = pd.DataFrame(on_deal_list, columns=['ФИО'])
#print(on_deal_list)
funcs.write_df('output.xlsx', temp_df)
