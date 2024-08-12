def pivot_tables(df, cols:str =  'Row', values:str = 'Word'):

    return df.pivot(columns=cols, values=values)

def shuffle_column(column):
    return np.random.permutation(column)

def create_card_id_list(df):

    num_of_rows = 5
    total_row_count = df.shape[0]
    num_of_cards = int(total_row_count/num_of_rows) + 1
    number_list = list(range(1, num_of_cards))

    df_new = pd.DataFrame({
        'RowNumber': number_list
    })

    return df_new

def add_card_id(df):

    #create card list nu
    card_ids = create_card_id_list(df)
    columns = ['Card', 'Row', 'Word']

    # Create an empty DataFrame with these column names
    df_shuffle = pd.DataFrame(columns=columns)

    for num in range(1,6):
        df_row_filter = df[df['Row'] == str(num)]
        df_row_filter['Row'] = shuffle_column(pivot_df['Row'].values)
        df_row_filter['Card'] = card_ids
        df_combined = pd.concat([df_shuffle, df_row_filter], ignore_index=True)

    return df_shuffle