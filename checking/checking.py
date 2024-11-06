import csv
import pandas as pd
import numpy as np
from func.functions import *

#variables
cards_per_print = 18
words_per_card = 5

df = pd.read_csv('data/241008_words.csv')
df_final = uppercase_words(df)

#checks
check_dups(df_final)
print(count_df(df_final))

