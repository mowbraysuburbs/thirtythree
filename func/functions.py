import csv
import pandas as pd
import numpy as np
import re


def choose_colour(df, colour):
    df['Colour'] = df['Colour'].astype(str)
    df['Row'] = df['Row'].astype(str)
    df['Word'] = df['Word'].str.upper()

    df_drop = df.drop(columns=['Tag 1', 'Tag 2', 'Tag 3', 'South Africa'])
    df_clr = df_drop[df_drop['Colour'] == str(colour)]

    return df_clr

def shuffle_column(column):
    return np.random.permutation(column)

def create_card_id_list(df):

    num_of_rows = 5
    total_row_count = df.shape[0]
    num_of_cards = int(total_row_count/num_of_rows) + 1
    number_list = list(range(1, num_of_cards))
    df_new = shuffle_column(number_list)

    return df_new

def add_card_id(df):

    #create card list nu
    card_ids = create_card_id_list(df)
    columns = ['Card', 'Row', 'Word']

    # Create an empty DataFrame with these column names
    df_shuffle = pd.DataFrame(columns=columns)

    for num in range(1,6):
        df_row_filter = df[df['Row'] == str(num)].copy()
        df_row_filter['Card'] = card_ids
        df_shuffle = pd.concat([df_shuffle, df_row_filter], ignore_index=True)

    return df_shuffle


def pivot_tables(df, card:str = 'Card' , cols:str =  'Row', values:str = 'Word'):

    df_card_id = add_card_id(df)

    return df_card_id.pivot(index =  card,columns=cols, values=values)

def check_fr_cherades(df, word):

    if df.empty:
        print('empty df')
        return True

    escaped_word = re.escape(word)
    contains_substr = df.apply(lambda row: row.astype(str).str.count(escaped_word).sum() > 1, axis=1).any()

    if contains_substr:
        return False
    
    else:
        print('contains multiple cherades-type words')
        return True


def cherades_table(df, word):

    word = re.escape(word)

    return df[df.apply(lambda row: row.astype(str).str.contains(word).any(), axis=1)]


def shorten_tables(df, perc):

    rows_to_keep = int(round(len(df) * (perc),0))

    #check 
    short_tbl = df.head(rows_to_keep)

    if len(short_tbl) % 5 > 0:

        return f"Sort out dataset number {len(short_tbl)} left over"
    
    else:

        return short_tbl