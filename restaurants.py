import pandas as pd

def generate_restaurant_df(filepath="restaurant_data/restaurant_data.xlsx"):
    df = pd.read_excel(filepath)

    if 'Cuisine' in df.columns and isinstance(df['Cuisine'].iloc[0], str):
        df['Cuisine'] = df['Cuisine'].apply(lambda x: eval(x) if isinstance(x, str) and x.startswith('[') else x)

    if 'Food' in df.columns and isinstance(df['Food'].iloc[0], str):
        df['Food'] = df['Food'].apply(lambda x: eval(x) if isinstance(x, str) and x.startswith('[') else x)

    return df