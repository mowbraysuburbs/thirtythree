import csv
import pandas as pd
import numpy as np
import re


def uppercase_words(df):
    df['Colour'] = df['Colour'].astype(str)
    # df['Row'] = df['Row'].astype(str)
    df['Word'] = df['Word'].str.upper()

    return df


def check_dups(df):
    duplicates = df[df.duplicated(subset='Word', keep='first')]

    if not duplicates.empty:
        dup_words = duplicates['Word'].tolist()
        return print(f"{len(dup_words)} duplicated words: {dup_words}")

    return print('no duplicates')


def shuffle_id_column(column):
    return np.random.permutation(column)

def shuffle_words(df):
    return df.sample(frac=1).reset_index(drop=True)


def colour_select(df, colour):

    df_drop = df.drop(columns=['Tag 2', 'Tag 3', 'South Africa'])
    df_clr = df_drop[df_drop['Colour'] == str(colour)]

    return df_clr


def create_card_id_list(num_of_cards):

    number_list = list(range(1, num_of_cards+1))
    df_new = shuffle_id_column(number_list)

    return df_new

def add_card_id(df, num_of_cards):

    #create card list nu
    card_ids = create_card_id_list(num_of_cards)
    columns = ['Card', 'Row', 'Word', 'Tag 1', 'Colour']

    # Create an empty DataFrame with these column names
    df_final = pd.DataFrame(columns=columns)

    for num in range(1,6):
        df_row_filter = df[df['Row'] == num].copy()
        df_row_filter['Card'] = card_ids
        df_final = pd.concat([df_final, df_row_filter], ignore_index=True)

    return df_final


def pivot_table(df, card:str = 'Card' , cols:str =  'Row', values:str = 'Word'):

    return df.pivot(index =  card,columns=cols, values=values)

def check_fr_charades(df, word):

    count = 1

    if df.empty:

        print(f'Iteration: {count}')
        count += 1
        return True

    escaped_word = re.escape(word)
    contains_substr = df.apply(lambda row: row.astype(str).str.count(escaped_word).sum() > 2, axis=1).any()

    if contains_substr:
        count += 1
        print(f'Iteration: {count}')
        return True
    
    else:
        return False


def charades_table(df, word):

    word = re.escape(word)

    return df[df.apply(lambda row: row.astype(str).str.contains(word).any(), axis=1)]

def save_csv(df, filename):
    df.to_csv(f'output/{filename}.csv', index=True, mode='w')


def word_number_order(multiplier):
    base_list = [1, 2, 3, 4, 5]
    return (base_list * multiplier)[:5 * multiplier]

def count_df(df):
    return df.shape[0]

def total_prints(df_length, cards, words):
    return int(df_length/(cards*words))

def shorten_table(df, length):
    return df.iloc[:length]

def total_words(pages, num_of_cards,num_of_words):
    return pages*num_of_cards*num_of_words

def num_of_cards(df_length, num_of_words):
    return int(df_length/num_of_words)