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

for i in range(0,2):

    #filter sides
    clr_1 = colour_select(df_final, i)
    clr_1_total = count_df(clr_1)

    #specs
    df_length = count_df(clr_1)
    pages = total_prints(df_length, cards_per_print, words_per_card)
    cards = num_of_cards(clr_1_total, words_per_card)
    words = total_words(pages, cards, words_per_card)

    #finalise data
    shuffle = shuffle_words(clr_1)
    final_rawdata = shorten_table(shuffle, words)

    #shuffle data and add row numbers
    num_list = word_number_order(cards)
    another_shuffle = shuffle_words(final_rawdata)
    another_shuffle['Row'] = num_list

    #find difficulty total
    card_id = add_card_id(another_shuffle, cards)
    card_id['Difficulty_total'] = card_id.groupby('Card')['Difficulty'].transform('sum')

    target_diff = {
        7: 70,
        8: 70,
        9: 70,
    }
    
    result = sort_difficulity(card_id, target_diff, 10)

    final = pivot_table(result).sort_values(by=('Difficulty_total', 1), ascending=False)
    save_csv(final, f'final_{i}')