import csv
import pandas as pd
import numpy as np
from func.functions import *

#get data
df = pd.read_csv('data/241115_words.csv')
df_final = uppercase_words(df)

#variables
cards_per_print = 18
words_per_card = 5

#checks
check_dups(df_final)
print(count_df(df_final))

#filter sides
clr_1 = colour_select(df_final, 0)
clr_1_total = count_df(clr_1)

#specs
pages = total_prints(clr_1, cards_per_print, words_per_card)
cards = num_of_cards(clr_1_total, words_per_card)
words = total_words(pages, cards, words_per_card)

#finalise data
shuffle = shuffle_words(clr_1)
final_rawdata = shorten_table(shuffle, words)

#assigning row number to words
num_list = word_number_order(cards)

another_shuffle = shuffle_words(final_rawdata)
another_shuffle['Row'] = num_list

card_id = add_card_id(another_shuffle, cards)
card_id['Difficulty_total'] = card_id.groupby('Card')['Difficulty'].transform('sum')

# target_diff = {
#     7: [25,35],
#     8: [55,65],
#     9: [65,75],
# }

# def even_distribute(df, clr_1_num_of_cards, target_diff):

#     columns = ['Card', 'Row', 'Word', 'Tag 1', 'Colour', 'Difficulty_total']
#     perfect = pd.DataFrame(columns=columns)    

#     for i in target_diff:

#     perfect = df[df['Difficulty_total'] == target_diff]
#     outliers = df[(df['Difficulty_total'] < target_diff) | (df['Difficulty_total'] > target_diff)]
#     ##################

#     # divide cards into different types
#     new_tech = outliers.loc[outliers['Tag 1'] == 'Technical']
#     new_other = outliers.loc[outliers['Tag 1'] != 'Technical']

#     new_tech['Row'] = row_no_tech

#     #other cards
#     new_other_count_df = count_df(outliers)
#     new_tech_count_df = count_df(new_tech)
#     # clr_1_other_shuffle = shuffle_words(new_other)

#     #assigning row number to words
#     new_num_list = word_number_order(int(new_other_count_df/5))

#     for _ in range(new_tech_count_df):
#         if row_no_tech in new_num_list:
#             new_num_list.remove(row_no_tech)

#     new_other_shuffle = shuffle_words(new_other)
#     new_other_shuffle['Row'] = new_num_list

#     # print(new_other_shuffle)

#     # perfect_final = perfect.drop(columns='column_name', inplace=True)

#     new_combined =  pd.concat([perfect, new_tech, new_other_shuffle], ignore_index=True)
#     new_combined.drop(columns='Card', inplace=True)

#     # print(new_combined)

#     new_card_id = add_card_id(new_combined, clr_1_num_of_cards)
#     new_card_id['Difficulty_total'] = new_card_id.groupby('Card')['Difficulty'].transform('sum')

#     ##################
#     return new_card_id

# result = clr_1_card_id  # Start with the initial input
# for _ in range(15):  # Repeat 5 iterations
#     result = even_distribute(result, clr_1_num_of_cards)


# new_clr_1_final = pivot_table(result).sort_values(by=('Difficulty_total', 1), ascending=False)
# new_clr_1_final.to_csv('all_words_stage2.csv', index=False)

# clr_1_tech = check_special_words(clr_1_final ,"[")

# clr_1_others = (
#     clr_1_final
#     .merge(
#         clr_1_tech, 
#         on=clr_1_final.columns.tolist(), 
#         how='left', 
#         indicator=True
#     )
#     .query('_merge == "left_only"')
#     .drop(columns=['_merge'])
# )

# clr_1_normal = clr_1_others.iloc[18:]
# save_csv(clr_1_normal, 'orange_normal')