import csv
import pandas as pd
import numpy as np
from func.functions import *

#variables
cards_per_print = 18
words_per_card = 5

df = pd.read_csv('data/240901_words.csv')
df_final = uppercase_words(df)

#checks
check_dups(df_final)
print(count_df(df_final))

clr_2 = colour_select(df_final, 1)

clr_2_orig_total = count_df(clr_2)

clr_2_charades = clr_2.loc[clr_2['Tag 1'] == 'Actions']
clr_2_other = clr_2.loc[clr_2['Tag 1'] != 'Actions']

#charades
clr_2_charades_orig_total = count_df(clr_2_charades)
clr_2_charades_pages = total_prints(clr_2_charades_orig_total, cards_per_print, 1)
clr_2_charades_new_words_total = total_words(clr_2_charades_pages, cards_per_print, 1)

clr_2_charades_shuffle = shuffle_words(clr_2_charades)
clr_2_charades_filtered = shorten_table(clr_2_charades_shuffle, clr_2_charades_new_words_total)

#other cards
clr_2_other_orig_total = count_df(clr_2_other) + clr_2_charades_new_words_total #add the charades words here
clr_2_other_pages = total_prints(clr_2_other_orig_total, cards_per_print, words_per_card)

clr_2_other_pages_new_words_total = total_words(clr_2_other_pages, cards_per_print, words_per_card)
clr_2_num_of_cards = num_of_cards(clr_2_other_pages_new_words_total, words_per_card)

clr_2_other_shuffle = shuffle_words(clr_2_other)
clr_2_other_filtered = shorten_table(
    clr_2_other_shuffle, 
    clr_2_other_pages_new_words_total - clr_2_charades_new_words_total
) 


clr_2_final = pd.DataFrame() # initally blank

while check_fr_charades(clr_2_final, '*'):

    clr_2_combined = pd.concat([clr_2_charades_filtered, clr_2_other_filtered], ignore_index=True)
    clr_2_shuffle = shuffle_words(clr_2_combined)

    clr_2_word_num_list = word_number_order(clr_2_num_of_cards)
    clr_2_shuffle['Row'] = clr_2_word_num_list

    clr_2_card_id = add_card_id(clr_2_shuffle, clr_2_num_of_cards)
    clr_2_final = pivot_table(clr_2_card_id)

    clr_2_charades = charades_table(clr_2_final ,"*")

    clr_2_others = (
        clr_2_final
        .merge(clr_2_charades, on=clr_2_final.columns.tolist(), how='left', indicator=True)
        .query('_merge == "left_only"')
        .drop(columns=['_merge'])
    )

    clr_2_times_two = clr_2_others.iloc[0:18]
    clr_2_normal = clr_2_others.iloc[18:18*clr_2_num_of_cards]


save_csv(clr_2_charades, 'colour_2_charades')
save_csv(clr_2_times_two, 'colour_2_times_two')
save_csv(clr_2_normal, 'colour_2_normal')

