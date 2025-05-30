import csv
import pandas as pd
import numpy as np
import re


def uppercase_words(df):
    df['Colour'] = df['Colour'].astype(str)
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
    print(f"Total words per side: {df_clr.shape[0]}")
    return df_clr


def create_card_id_list(num_of_cards):
    number_list = list(range(1, num_of_cards + 1))
    return number_list


def add_card_id(df, num_of_cards):
    card_ids = create_card_id_list(num_of_cards)
    columns = ['Card', 'Row', 'Word', 'Tag 1', 'Colour']
    df_final = pd.DataFrame(columns=columns)
    for num in range(1, 6):
        df_row_filter = df[df['Row'] == num].copy()
        df_row_filter['Card'] = card_ids
        df_final = pd.concat([df_final, df_row_filter], ignore_index=True)
    return df_final


def pivot_table(df, card: str = 'Card', cols: str = 'Row', values: list = ['Word', 'Difficulty_total']):
    return df.pivot(index=card, columns=cols, values=values).reset_index(drop=True)


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


def check_special_words(df, word):
    word = re.escape(word)
    return df[df.apply(lambda row: row.astype(str).str.contains(word).any(), axis=1)]


def save_csv(df, filename):
    df.to_csv(f'{filename}.csv', index=False, mode='w')


def word_number_order(multiplier):
    base_list = [1, 2, 3, 4, 5]
    return (base_list * multiplier)[:5 * multiplier]


def count_df(df):
    return int(df.shape[0])


def total_prints(df_length, cards, words):
    return int(df_length / (cards * words))


def shorten_table(df, length):
    return df.iloc[:length]


def total_words(pages, num_of_cards, num_of_words):
    return int(pages * num_of_cards * num_of_words)


def num_of_cards(df_length, num_of_words):
    return int(df_length / num_of_words)


def sort_difficulity(df, diff_limits, attempts):
    result = pd.DataFrame(columns=df.columns)
    remaining_df = df.copy()

    for attempt in range(1, attempts + 1):
        if len(remaining_df) == 0:
            print('All words have been added')
            break
        unique_cards = remaining_df['Card'].unique()
        for card in unique_cards:
            card_all = remaining_df[remaining_df['Card'] == card]
            card_diff = card_all['Difficulty_total'].values[0]
            if card_diff in diff_limits:
                if len(result[result['Difficulty_total'] == card_diff]) < diff_limits[card_diff] * 5:
                    result = pd.concat([result, card_all], ignore_index=False).drop_duplicates()

        filter_cols = ['Card', 'Row', 'Word', 'Tag 1', 'Colour', 'Difficulty', 'Length']
        result_keys = result[filter_cols]
        remaining_df = (
            remaining_df[~remaining_df[filter_cols]
            .isin(result_keys.to_dict(orient='list'))
            .all(axis=1)]
        )

        # Drop the specified columns
        filter_cols2 = ['Word', 'Tag 1', 'Colour', 'Difficulty', 'Length']
        leftover_cols = remaining_df['Card']
        leftover_rows = remaining_df['Row']
        # Shuffle the remaining DataFrame
        remaining_df = shuffle_words(remaining_df[filter_cols2])
        remaining_df['Row'] = leftover_rows.values
        remaining_df['Card'] = leftover_cols.values

        remaining_df['Difficulty_total'] = remaining_df.groupby('Card')['Difficulty'].transform('sum')

        if attempt == attempts:
            print(f'Words left: {len(remaining_df)}')
            remaining_df['Difficulty_total'] = remaining_df.groupby('Card')['Difficulty'].transform('sum')
            result = pd.concat([result, remaining_df], ignore_index=True).drop_duplicates()

    return result