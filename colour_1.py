import csv
import pandas as pd
import numpy as np
from func.functions import *

#variables
cards_per_print = 18
words_per_card = 5

# final_output = pd.DataFrame() # initally blank

df = pd.read_csv('data/240901_words.csv')
df_final = uppercase_words(df)

#checks
check_dups(df_final)
print(count_df(df_final))

# card colour 1 
clr_1 = colour_select(df_final, 0)
clr_1_orig_total = count_df(clr_1)
clr_1_pages = total_prints(clr_1_orig_total, cards_per_print, words_per_card)
clr_1_new_words_total = total_words(clr_1_pages, cards_per_print, words_per_card)
clr_1_num_of_cards = num_of_cards(clr_1_new_words_total, words_per_card)

clr_1_shuffle = shuffle_words(clr_1)

clr_1_filtered = shorten_table(clr_1_shuffle, clr_1_new_words_total)

clr_1_word_num_list = word_number_order(clr_1_num_of_cards)

clr_1_filtered['Row'] = clr_1_word_num_list
clr_1_card_id = add_card_id(clr_1_filtered, clr_1_num_of_cards)
clr_1_final = pivot_table(clr_1_card_id)

clr_1_charades = clr_1_final.iloc[0:18]
clr_1_times_two = clr_1_final.iloc[18:18*2]
clr_1_normal = clr_1_final.iloc[18*2:clr_1_new_words_total]

save_csv(clr_1_charades, 'colour_1_charades')
save_csv(clr_1_times_two, 'colour_1_times_2')
save_csv(clr_1_normal, 'colour_1_normal')

# card colour 2

# while check_fr_charades(final_output, '*'):

