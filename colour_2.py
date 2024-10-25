import csv
import pandas as pd
import numpy as np
from func.functions import *

#variables
cards_per_print = 18
words_per_card = 5

df = pd.read_csv('data/241022_words.csv')
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

#special words

row_no = int(5)

##technical 
clr_2_tech_orig_total = count_df(clr_2_tech)
clr_2_tech_pages = total_prints(clr_2_tech_orig_total, cards_per_print, 1)
clr_2_tech_new_words_total = total_words(clr_2_tech_pages, cards_per_print, 1)

clr_2_tech_filtered = shorten_table(
    clr_2_tech, 
    clr_2_tech_new_words_total,
)

#selecting position on card
clr_2_tech_filtered['Row'] = row_no
# print(clr_2_tech_filtered)

##charades
clr_2_charades_orig_total = count_df(clr_2_charades)
clr_2_charades_pages = total_prints(clr_2_charades_orig_total, cards_per_print, 1)
clr_2_charades_new_words_total = total_words(clr_2_charades_pages, cards_per_print, 1)

clr_2_charades_filtered = shorten_table(
    clr_2_charades, 
    clr_2_charades_new_words_total,
)

#selecting position on card
clr_2_charades_filtered['Row'] = row_no
# print(clr_2_charades_filtered)

#other cards
clr_2_other_orig_total = (
    count_df(clr_2_other) 
    + clr_2_charades_orig_total 
    + clr_2_tech_orig_total
)


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
    words_per_card
)

clr_2_other_shuffle = shuffle_words(clr_2_other)
clr_2_other_filtered = shorten_table(
    clr_2_other_shuffle, 
    clr_2_other_pages_new_words_total - clr_2_tech_new_words_total - clr_2_charades_new_words_total
) 


#assigning row number to words
clr_2_word_num_list = word_number_order(clr_2_num_of_cards)

total_removed_rows = clr_2_tech_filtered.shape[0] + clr_2_charades_filtered.shape[0]

# print(len(clr_2_word_num_list))

for _ in range(total_removed_rows):
    if row_no in clr_2_word_num_list:
        clr_2_word_num_list.remove(row_no)

# print(len(clr_2_word_num_list))

clr_2_other_shuffle = shuffle_words(clr_2_other_filtered)

# print(clr_2_other_shuffle.count())
clr_2_other_shuffle['Row'] = clr_2_word_num_list

clr_2_combined = pd.concat([clr_2_other_shuffle, clr_2_charades_filtered, clr_2_tech_filtered], ignore_index=True)

clr_2_card_id = add_card_id(clr_2_combined, clr_2_num_of_cards)

clr_2_final = pivot_table(clr_2_card_id)

#sprting words to different catefocry
clr_2_charades_final = check_special_words(clr_2_final ,"*")

clr_2_tech_final = check_special_words(clr_2_final ,"[")
# print(clr_2_tech_final.columns)

clr_2_others = (
    clr_2_final
    .merge(
        clr_2_tech_final, 
        on=clr_2_final.columns.tolist(), 
        how='left', 
        indicator=True
    )
    .query('_merge == "left_only"')
    .drop(columns=['_merge'])
    .merge(
        clr_2_charades_final, 
        on=clr_2_final.columns.tolist(), 
        how='left', 
        indicator=True
    )
    .query('_merge == "left_only"')
    .drop(columns=['_merge'])
)

#done afterwards so i can do the antijoin above
clr_2_tech_final[1], clr_2_tech_final[5] = clr_2_tech_final[5], clr_2_tech_final[1]

clr_2_times_two = clr_2_others.iloc[0:18]
clr_2_normal = clr_2_others.iloc[18:]

save_csv(clr_2_tech_final, 'blue_tech')
save_csv(clr_2_times_two, 'blue_times_two')
save_csv(clr_2_charades_final, 'blue_charades')
save_csv(clr_2_normal, 'blue_normal')


