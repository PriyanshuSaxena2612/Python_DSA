import pandas as pd

def find_classes(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby('class', as_index = False)['student'].nunique().rename(columns = {
        'student': 'count'
    }).query('count >= 5')[['class']]
