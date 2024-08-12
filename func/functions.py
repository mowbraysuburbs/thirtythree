import csv
import pandas as pd
import numpy as np


def choose_colour(df, colour):
    df['Colour'] = df['Colour'].astype(str)
    df['Row'] = df['Row'].astype(str)
    # df['Colour_Row'] = df['Colour'] + '-' + df['Row']
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