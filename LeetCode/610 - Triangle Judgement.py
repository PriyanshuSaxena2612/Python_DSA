import pandas as pd

def triangle_judgement(df: pd.DataFrame) -> pd.DataFrame:
    df['triangle'] = (
        (df['x'] + df['y'] > df['z']) &
        (df['x'] + df['z'] > df['y']) &
        (df['z'] + df['y'] > df['x']) 
    ).map({True: 'Yes', False: 'No'})
    return df
    
