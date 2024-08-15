import csv
import pandas as pd
import numpy as np
from func.functions import *

df = pd.read_csv('data/words_r2.csv')
final_output = pd.DataFrame() # initally blank

while check_fr_cherades(final_output, '*'):
    df_clr_1 = choose_colour(df,0)
    df_clr_2 = choose_colour(df,1)

    final_clr_1 = pivot_tables(df_clr_1)
    final_clr_2 = pivot_tables(df_clr_2)

    cherades = cherades_table(final_clr_2 ,"*")

    final_output = pd.concat([final_clr_1, final_clr_2], ignore_index=True)

cherades.to_csv('output/cherades.csv', index=True)
# final_clr_2.to_csv('colour_2.csv', index=True)
# final_clr_1.to_csv('colour_1.csv', index=True)
# final_clr_2.to_csv('colour_2.csv', index=True)