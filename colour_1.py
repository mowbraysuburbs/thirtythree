import csv
import pandas as pd
import numpy as np
from func.functions import *

#variables
cards_per_print = 18
words_per_card = 5

df = pd.read_csv('data/241115_words.csv')
df_final = uppercase_words(df)

#checks
check_dups(df_final)
print(count_df(df_final))

# card colour 1 
clr_1 = colour_select(df_final, 0)
clr_1_orig_total = count_df(clr_1)

# divide cards into different types
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
row_no_tech = int(1)
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
    words_per_card,
)

clr_1_other_shuffle = shuffle_words(clr_1_other)
clr_1_other_filtered = shorten_table(
    clr_1_other_shuffle, 
    clr_1_other_pages_new_words_total - clr_1_tech_new_words_total
)  


#assigning row number to words
clr_1_word_num_list = word_number_order(clr_1_num_of_cards)

for _ in range(clr_1_tech_filtered.shape[0]):
    if row_no_tech in clr_1_word_num_list:
        clr_1_word_num_list.remove(row_no_tech)

clr_1_other_shuffle = shuffle_words(clr_1_other_filtered)
clr_1_other_shuffle['Row'] = clr_1_word_num_list

clr_1_combined = pd.concat([clr_1_other_shuffle, clr_1_tech_filtered], ignore_index=True)

clr_1_card_id = add_card_id(clr_1_combined, clr_1_num_of_cards)
clr_1_card_id['Difficulty_total'] = clr_1_card_id.groupby('Card')['Difficulty'].transform('sum')

clr_1_final = pivot_table(clr_1_card_id).sort_values(by=('Difficulty_total', 1), ascending=False)
clr_1_final.to_csv('all_words.csv', index=False)

def even_distribute(df, clr_1_num_of_cards):

    target_diff = 9

    perfect = df[df['Difficulty_total'] == target_diff]
    outliers = df[(df['Difficulty_total'] < target_diff) | (df['Difficulty_total'] > target_diff)]
    ##################

    # divide cards into different types
    new_tech = outliers.loc[outliers['Tag 1'] == 'Technical']
    new_other = outliers.loc[outliers['Tag 1'] != 'Technical']

    new_tech['Row'] = row_no_tech

    #other cards
    new_other_count_df = count_df(outliers)
    new_tech_count_df = count_df(new_tech)
    # clr_1_other_shuffle = shuffle_words(new_other)

    #assigning row number to words
    new_num_list = word_number_order(int(new_other_count_df/5))

    for _ in range(new_tech_count_df):
        if row_no_tech in new_num_list:
            new_num_list.remove(row_no_tech)

    new_other_shuffle = shuffle_words(new_other)
    new_other_shuffle['Row'] = new_num_list

    # print(new_other_shuffle)

    # perfect_final = perfect.drop(columns='column_name', inplace=True)

    new_combined =  pd.concat([perfect, new_tech, new_other_shuffle], ignore_index=True)
    new_combined.drop(columns='Card', inplace=True)

    # print(new_combined)

    new_card_id = add_card_id(new_combined, clr_1_num_of_cards)
    new_card_id['Difficulty_total'] = new_card_id.groupby('Card')['Difficulty'].transform('sum')

    ##################
    return new_card_id

result = clr_1_card_id  # Start with the initial input
for _ in range(15):  # Repeat 5 iterations
    result = even_distribute(result, clr_1_num_of_cards)


new_clr_1_final = pivot_table(result).sort_values(by=('Difficulty_total', 1), ascending=False)
new_clr_1_final.to_csv('all_words_stage2.csv', index=False)

clr_1_tech = check_special_words(clr_1_final ,"[")

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

# clr_1_normal = clr_1_others.iloc[18:]
# save_csv(clr_1_normal, 'orange_normal')