import csv
import pandas as pd
import numpy as np
from func.functions import *

# df = pd.read_csv('data/240830_words.csv')
# total_cards_per_page = 18

df_charades_no_action = pd.read_csv('test/charades_test_no_actions.csv')
df_charades_has_action = pd.read_csv('test/charades_test_has_actions.csv')

print(check_fr_charades(df_charades_no_action, '*'))
print(check_fr_charades(df_charades_has_action, '*'))
# print(correct_df_shape(df, total_cards_per_page))
