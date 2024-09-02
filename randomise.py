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

clr_2 = colour_select(df_final, 1)

clr_2_orig_total = count_df(clr_2)

clr_2_charades = clr_2.loc[clr_2['Tag 1'] == 'Actions']
clr_2_other = clr_2.loc[clr_2['Tag 1'] != 'Actions']

clr_2_charades_orig_total = count_df(clr_2_charades)
clr_2_charades_pages = total_prints(clr_2_charades_orig_total, cards_per_print, 1)
clr_2_charades_new_words_total = total_words(clr_2_charades_pages, cards_per_print, 1)

clr_2_charades_filtered = shorten_table(clr_2_charades, clr_2_charades_new_words_total)

clr_2_other_orig_total = count_df(clr_2_other) + clr_2_charades_new_words_total
clr_2_other_pages = total_prints(clr_2_other_orig_total, cards_per_print, words_per_card)
clr_2_other_pages_new_words_total = total_words(clr_2_other_pages, cards_per_print, words_per_card)

clr_2_other_filtered = shorten_table(clr_2_other, clr_2_other_pages_new_words_total)

clr_2_combined = pd.concat([clr_2_charades_filtered, clr_2_other_filtered], ignore_index=True)

clr_1_num_of_cards = num_of_cards(clr_1_new_words_total, words_per_card)

clr_2_shuffle = shuffle_words(clr_2_combined)

clr_2_word_num_list = word_number_order(clr_2_other_pages_new_words_total)

clr_1_filtered['Row'] = clr_2_word_num_list
clr_1_card_id = add_card_id(clr_2_combined, clr_1_num_of_cards)
clr_1_final = pivot_table(clr_1_card_id)

clr_1_charades = clr_1_final.iloc[0:18]
clr_1_times_two = clr_1_final.iloc[18:18*2]
clr_1_normal = clr_1_final.iloc[18*2:clr_1_new_words_total]

save_csv(clr_1_charades, 'colour_1_charades')
save_csv(clr_1_times_two, 'colour_1_times_2')
save_csv(clr_1_normal, 'colour_1_normal')

# print(clr_2_charades)

    # clr_2_other_pages = total_prints(clr_1_orig_total, cards_per_print, words_per_card)
    # clr_2_new_words_total = total_words(clr_1_pages, cards_per_print, words_per_card)
    # clr_2_num_of_cards = num_of_cards(clr_1_new_words_total, words_per_card)

    # clr_1_shuffle = shuffle_words(clr_1)

#     #colour 1 
#     clr_1_cherades = final_clr_1.iloc[0:19]
#     clr_1_times_two = final_clr_1.iloc[18:18*2]
#     clr_1_normal = final_clr_1.iloc[18*2:18*5]

#     #colour 2
#     clr_2_cherades = cherades_table(final_clr_2 ,"*")

#     clr_2_others = (
#         final_clr_2
#         .merge(clr_2_cherades, on=final_clr_2.columns.tolist(), how='left', indicator=True)
#         .query('_merge == "left_only"')
#         .drop(columns=['_merge'])
#     )

#     clr_2_times_two = clr_2_others.iloc[0:18]
#     clr_2_normal = clr_2_others.iloc[18:18*4]

#     #check
#     final_output = pd.concat([final_clr_1, final_clr_2], ignore_index=True)


# save_csv(clr_1_cherades, 'colour_1_cherades')
# save_csv(clr_1_times_two, 'colour_1_times_2')
# save_csv(clr_1_normal, 'colour_1_normal')

# save_csv(clr_2_cherades, 'colour_2_cherades')
# save_csv(clr_2_times_two, 'colour_2_times_2')
# save_csv(clr_2_normal, 'colour_2_normal')