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

card_id = add_card_id(another_shuffle, cards)
card_id['Difficulty_total'] = card_id.groupby('Card')['Difficulty'].transform('sum')

target_diff = {
    7: 35,
    8: 35,
    9: 70,
}

def adjust_difficulty(df, target_diff):
    result = pd.DataFrame()
    remaining_df = df.copy()
    
    for difficulty, amount in target_diff.items():

        print(f"Difficulty: {difficulty}, Amount: {amount}")
        attempts = 0
        max_attempts = 10  # Set a maximum number of attempts to avoid infinite loops
    #     while len(result[result['Difficulty_total'] == difficulty]) <= amount:
    #         if attempts >= max_attempts or remaining_df.empty:
    #             print(f"Cannot satisfy the criteria for difficulty {difficulty} with amount {amount}.")
    #             break
    #         shuffled_df = shuffle_words(remaining_df)
    #         shuffled_df['Row'] = word_number_order(len(shuffled_df))
    #         card_id = add_card_id(shuffled_df, cards)
    #         card_id['Difficulty_total'] = card_id.groupby('Card')['Difficulty'].transform('sum')
            
    #         for i in range(len(card_id)):
    #             if card_id['Difficulty_total'][i] == difficulty:
    #                 result = pd.concat([result, card_id.iloc[i:i+1]]).drop_duplicates()
    #                 remaining_df = card_id[~card_id.index.isin(result.index)]
            
    #         attempts += 1
    #         print(f"Attempts: {attempts}, Difficulty: {difficulty}, Result size: {len(result)}")
    
    # # Add remaining words to the result without exceeding the difficulty limit
    # result = pd.concat([result, remaining_df]).drop_duplicates()
    
    return result


# # Adjust difficulty and get the final DataFrame
adjusted_df = adjust_difficulty(card_id, target_diff)
# print(adjusted_df.head())

# # Save the final DataFrame to a CSV file
# adjusted_df.to_csv('adjusted_words.csv', index=False)