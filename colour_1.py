import csv
import pandas as pd
import numpy as np
from func.functions import *

#variables
cards_per_print = 18
words_per_card = 5


# df = pd.read_csv('data/240922_words.csv')
df = pd.read_csv('test/tech_word_test.csv')
df_final = uppercase_words(df)

#checks
check_dups(df_final)
print(count_df(df_final))

# card colour 1 
clr_1 = colour_select(df_final, 0)
clr_1_orig_total = count_df(clr_1)

clr_1_tech = clr_1.loc[clr_1['Tag 1'] == 'Technical']
clr_1_other = clr_1.loc[clr_1['Tag 1'] != 'Technical']

#technical 
clr_1_tech_orig_total = count_df(clr_1_tech)
clr_1_tech_pages = total_prints(clr_1_tech_orig_total, cards_per_print, 1)
clr_1_tech_new_words_total = total_words(clr_1_tech_pages, cards_per_print, 1)

clr_1_tech_filtered = shorten_table(
    clr_1_tech, 
    clr_1_tech_new_words_total,
)

#selecting position on card
row_no_tech = int(5)
clr_1_tech_filtered['Row'] = row_no_tech


#other cards
clr_1_other_orig_total = count_df(clr_1_other) + clr_1_tech_new_words_total #add the list words here

clr_1_other_pages = total_prints(
    clr_1_other_orig_total, 
    cards_per_print, 
    words_per_card
)

clr_1_other_pages_new_words_total = total_words(
    clr_1_other_pages, 
    cards_per_print, 
    words_per_card
)

clr_1_num_of_cards = num_of_cards(
    clr_1_other_pages_new_words_total, 
    words_per_card
)

clr_1_other_shuffle = shuffle_words(clr_1_other)
clr_1_other_filtered = shorten_table(
    clr_1_other_shuffle, 
    clr_1_other_pages_new_words_total - clr_1_tech_new_words_total
) 

#assigning row number to words
clr_2_word_num_list = word_number_order(clr_1_num_of_cards)

for _ in range(clr_1_tech_filtered.shape[0]):
    clr_2_word_num_list.remove(row_no_tech)

clr_1_other_shuffle = shuffle_words(clr_1_other_filtered)
clr_1_other_shuffle['Row'] = clr_2_word_num_list

clr_1_combined = pd.concat([clr_1_other_shuffle, clr_1_tech_filtered], ignore_index=True)

clr_1_card_id = add_card_id(clr_1_combined, clr_1_num_of_cards)
clr_1_final = pivot_table(clr_1_card_id)

clr_1_tech = charades_table(clr_1_final ,"[")

clr_1_others = (
    clr_1_final
    .merge(
        clr_1_tech, 
        on=clr_1_final.columns.tolist(), 
        how='left', 
        indicator=True
    )
    .query('_merge == "left_only"')
    .drop(columns=['_merge'])
)

clr_1_times_two = clr_1_others.iloc[0:18]
clr_1_charades = clr_1_others.iloc[18:18*clr_1_num_of_cards]
clr_1_normal = clr_1_others.iloc[18:]


save_csv(clr_1_tech, 'clr_1_tech')
save_csv(clr_1_times_two, 'clr_1_times_two')
save_csv(clr_1_charades, 'clr_1_charades')
save_csv(clr_1_normal, 'colour_1_normal')