import csv
import pandas as pd
import numpy as np
import datetime
from func.functions import *

#global
today = datetime.date.today().strftime('%Y%m%d')
card_colours ={
    0: 'orange',
    1: 'blue',
}

#variables
cards_per_print = 18
words_per_card = 5

target_diff = {
    7: 5,
    8: 160,
    9: 5,
}

#get and clean data
df = pd.read_csv('data/250413_words.csv')
df_final = uppercase_words(df)

#checks
check_dups(df_final)
print(count_df(df_final))

for colour in list(card_colours.keys()):

    #filter sides
    clr_1 = colour_select(df_final, colour)
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
    for i in range(10):
        another_shuffle = shuffle_words(another_shuffle)
    another_shuffle['Row'] = num_list

    #find difficulty total
    card_id = add_card_id(another_shuffle, cards)

    card_id['Difficulty_total'] = card_id.groupby('Card')['Difficulty'].transform('sum')

    result = sort_difficulity(card_id, target_diff, 30)

    final = (
        pivot_table(result)
        .sort_values(by=('Difficulty_total', 1), ascending=False)
    )

    save_csv(final, f'{today}_final_{card_colours[colour]}')

    print(
        f"{card_colours[colour]}\n",
        f"7: {final[final[('Difficulty_total', 1)] == 7.0].shape[0]} \n",
        f"8: {final[final[('Difficulty_total', 1)] == 8.0].shape[0]} \n",
        f"9: {final[final[('Difficulty_total', 1)] == 9.0].shape[0]} \n",    
    )



    
