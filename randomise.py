import csv
import pandas as pd
import numpy as np
from func.functions import pivot_tables, shuffle_column, create_card_id_list, add_card_id, choose_colour, check_fr_cherades

df = pd.read_csv('data/words_r2.csv')
final_output = pd.DataFrame() # initally blank

# while check_fr_cherades(final_output, '*'):
#     print('contains *')
#     df_clr_1 = choose_colour(df,0)
#     df_clr_2 = choose_colour(df,1)

#     final_clr_1 = pivot_tables(df_clr_1)
#     final_clr_2 = pivot_tables(df_clr_2)

#     final_output = pd.concat([final_clr_1, final_clr_2], ignore_index=True)

#     print('contains *')

# final_output.to_csv('output.csv', index=True)
print('contains *')
df_clr_1 = choose_colour(df,0)
df_clr_2 = choose_colour(df,1)

final_clr_1 = pivot_tables(df_clr_1)
final_clr_2 = pivot_tables(df_clr_2)

final_output = pd.concat([final_clr_1, final_clr_2], ignore_index=True)
# print(check_fr_cherades(final_output, '*'))
print(final_output)
# print(df_clr_1)
# print(create_card_id_list(df_clr_1))
# print(final_clr_1)