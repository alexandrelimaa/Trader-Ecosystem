import pandas as pd

def load_data(filename):
    df = pd.read_csv(filepath,
                     encoding='latin1',
                     sep=';',
                     thousands='.',
                     decimal=',',
                     )


def clean_data(df):
    df['datetime'] = pd.to_datetime(df['Data'] + ' ' + df['Time'], dayfirst = True)
    df = df.set_index('datetime')
    df = df.sort_index()
    return df