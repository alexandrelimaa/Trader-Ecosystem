import pandas as pd
import glob

def load_data(filename):
    df = pd.read_csv(filename,
                     encoding='latin1',
                     sep=';',
                     thousands='.',
                     decimal=',',
                     )
    return df

def clean_data(df):
    df['datetime'] = pd.to_datetime(df['Data'] + ' ' + df['Hora'], dayfirst = True)
    df = df.set_index('datetime')
    df = df.sort_index()
    return df

def load_all_files(pattern):
    filepaths = glob.glob(pattern)
    dataframes = [clean_data(load_data(fp)) for fp in filepaths]
    combined = pd.concat(dataframes)
    combined = combined.sort_index()
    return combined