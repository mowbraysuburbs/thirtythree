import csv
import pandas as pd
import numpy as np
from func.functions import *

df1 = pd.read_csv('data/241027_words.csv')
df1_final = uppercase_words(df1)

df2 = pd.read_csv('data/241022_words.csv')
df2_final = uppercase_words(df2)

outliers = (
    df1_final
    .merge(
        df2_final, 
        on=df2_final.columns.tolist(), 
        how='left', 
        indicator=True
    )
    .query('_merge == "right_only"')
    # .drop(columns=['_merge'])
)

print(outliers)

