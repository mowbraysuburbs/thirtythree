import csv
import pandas as pd
import numpy as np
from func.functions import *

#variables
cards_per_print = 18
words_per_card = 5

df = pd.read_csv('data/241029_words.csv')
df_final = uppercase_words(df)

#checks
check_dups(df_final)
print(count_df(df_final))

# card colour 2 
clr_2 = colour_select(df_final, 1)
clr_2_orig_total = count_df(clr_2)

# divide cards into different types
clr_2_charades = clr_2.loc[clr_2['Tag 1'] == 'Actions']
clr_2_other = clr_2.loc[clr_2['Tag 1'] != 'Actions']

#charadesnical 
clr_2_charades_orig_total = count_df(clr_2_charades)
clr_2_charades_pages = total_prints(clr_2_charades_orig_total, cards_per_print, 1)
clr_2_charades_new_words_total = total_words(clr_2_charades_pages, cards_per_print, 1)


clr_2_charades_filtered = shorten_table(
    clr_2_charades, 
    clr_2_charades_new_words_total,
)

#selecting position on card
row_no_charades = int(5)
clr_2_charades_filtered['Row'] = row_no_charades

#other cards
clr_2_other_orig_total = count_df(clr_2_other) + clr_2_charades_new_words_total #add the list words here

clr_2_other_pages = total_prints(
    clr_2_other_orig_total, 
    cards_per_print, 
    words_per_card
)

clr_2_other_pages_new_words_total = total_words(
    clr_2_other_pages, 
    cards_per_print, 
    words_per_card
)

clr_2_num_of_cards = num_of_cards(
    clr_2_other_pages_new_words_total, 
    words_per_card,
)

clr_2_other_shuffle = shuffle_words(clr_2_other)
clr_2_other_filtered = shorten_table(
    clr_2_other_shuffle, 
    clr_2_other_pages_new_words_total - clr_2_charades_new_words_total
) 

#assigning row number to words
clr_2_word_num_list = word_number_order(clr_2_num_of_cards)

for _ in range(clr_2_charades_filtered.shape[0]):
    if row_no_charades in clr_2_word_num_list:
        clr_2_word_num_list.remove(row_no_charades)

clr_2_other_shuffle = shuffle_words(clr_2_other_filtered)
clr_2_other_shuffle['Row'] = clr_2_word_num_list

clr_2_combined = pd.concat([clr_2_other_shuffle, clr_2_charades_filtered], ignore_index=True)


clr_2_card_id = add_card_id(clr_2_combined, clr_2_num_of_cards)
clr_2_final = pivot_table(clr_2_card_id)

clr_2_charades = check_special_words(clr_2_final ,"*")

clr_2_others = (
    clr_2_final
    .merge(
        clr_2_charades, 
        on=clr_2_final.columns.tolist(), 
        how='left', 
        indicator=True
    )
    .query('_merge == "left_only"')
    .drop(columns=['_merge'])
)

clr_2_times_two = clr_2_others.iloc[0:18]
clr_2_tech = clr_2_others.iloc[18:18*2]
clr_2_normal = clr_2_others.iloc[18*2:]


save_csv(clr_2_tech, 'blue_tech')
save_csv(clr_2_times_two, 'blue_times_two')
save_csv(clr_2_charades, 'blue_charades')
save_csv(clr_2_normal, 'blue_normal')