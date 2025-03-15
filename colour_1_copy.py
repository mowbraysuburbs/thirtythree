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
clr_1 = colour_select(df_final, 1)
clr_1_total = count_df(clr_1)

#specs
df_length = count_df(clr_1)
pages = total_prints(df_length, cards_per_print, words_per_card)
cards = num_of_cards(clr_1_total, words_per_card)
words = total_words(pages, cards, words_per_card)

#finalise data
shuffle = shuffle_words(clr_1)
final_rawdata = shorten_table(shuffle, words)

#assigning row number to words
num_list = word_number_order(cards)

another_shuffle = shuffle_words(final_rawdata)

another_shuffle['Row'] = num_list

# save_csv(another_shuffle, 'checking')

card_id = add_card_id(another_shuffle, cards)
card_id['Difficulty_total'] = card_id.groupby('Card')['Difficulty'].transform('sum')

# Sort card_id by Card column in asc. order
card_id = card_id.sort_values(by='Card', ascending=True)

# save_csv(card_id, 'checking')

result = pd.DataFrame(columns=card_id.columns)
remaining_df = card_id.copy()

target_diff = {
    7: 70,
    8: 70,
    9: 70,
}

counter = 1
attempt = 1
attempt_limit = 10


while attempt <= attempt_limit:
    # print(remaining_df)
    if len(remaining_df) == 0:
        break
    for index, row in remaining_df.iterrows():
        diff_row = int(row['Difficulty_total'])
        # print(diff_row)
        if diff_row in list(target_diff.keys()):
            # if not (len(result[result['Difficulty_total']] == diff_row) == target_diff[diff_row]):
            if len(result[result['Difficulty_total'] == diff_row]) <= target_diff[diff_row]*5:
                new_row = pd.DataFrame([row], columns=card_id.columns)
                # print(new_row)
                result = pd.concat([result, new_row], ignore_index=False).drop_duplicates()
                # print('new row added')
            else:
                print(f"Difficulty {diff_row} is full")
    #         # diff_num = row['Difficulty_total']
    #         # if diff_num in target_diff:
    # print(len(result))

    remaining_df = (
        pd.merge(
            remaining_df, 
            result, 
            on=list(card_id.columns), 
            how='outer', 
            indicator=True
        )
        .query('_merge == "left_only"')
        .drop('_merge', axis=1)
    )

    # print(remaining_df)
    leftover_cols = remaining_df['Card']
    leftover_rows = remaining_df['Row']
    remaining_df = shuffle_words(remaining_df.drop(columns=['Card', 'Difficulty_total', 'Row']))
    remaining_df['Row'] = leftover_rows.values
    remaining_df['Card'] = leftover_cols.values
    remaining_df['Difficulty_total'] = remaining_df.groupby('Card')['Difficulty'].transform('sum')

    # print(remaining_df)
    attempt +=1

    print(attempt, len(remaining_df))
    # if len(remaining_df) == 0:

# # remaining_df = card_id[~card_id.index.isin(result.index)]

# save_csv(card_id.sort_values(by='Card', ascending=True), 'card_id')
save_csv(remaining_df.sort_values(by='Difficulty_total', ascending=True), 'remaining_df')
save_csv(result.sort_values(by='Card', ascending=True), 'result')

final = pivot_table(result).sort_values(by=('Difficulty_total', 1), ascending=False)
save_csv(final, 'final')