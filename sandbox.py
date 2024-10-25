import csv
import pandas as pd
import numpy as np
from func.functions import *

#variables
cards_per_print = 18
words_per_card = 5

df = pd.read_csv('data/241016_words.csv')
df_final = uppercase_words(df)

#word lengh checks
check_dups(df_final)
print(count_df(df_final))

#split to selected colour
clr_2 = colour_select(df_final, 1)
clr_2_orig_total = count_df(clr_2)

#split into different word power/types
clr_2_charades = clr_2.loc[clr_2['Tag 1'] == 'Actions']
clr_2_tech = clr_2.loc[clr_2['Tag 1'] == 'Technical']
clr_2_other = clr_2.loc[ (clr_2['Tag 1'] != 'Actions') & (clr_2['Tag 1'] != 'Technical') ]

#word length check after split:
print(clr_2_other.shape[0]  + clr_2_charades.shape[0] + clr_2_tech.shape[0]  - int(clr_2_orig_total))

