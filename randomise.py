import csv
import pandas as pd
import numpy as np

df = pd.read_csv('words.csv')
df['Colour'] = df['Colour'].astype(str)
df['Row'] = df['Row'].astype(str)
# df['Colour_Row'] = df['Colour'] + '-' + df['Row']

df_drop = df.drop(columns=['Tag 1', 'Tag 2', 'Tag 3', 'South Africa'])

df_clr_1 = df_drop[df_drop['Colour'] == '1']
df_clr_2 = df_drop[df_drop['Colour'] == '0']






# pivot_clr_1 = pivot_tables(df_clr_1)

print(create_card_id_list(df_clr_1))