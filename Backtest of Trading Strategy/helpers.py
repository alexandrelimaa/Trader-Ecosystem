#Libraries
import pandas as pd
import glob


def load_data(filename):
    """ Load data from csv file in portuguese and input some changes to read the file"""
    df = pd.read_csv(filename,
                     encoding='latin1',
                     sep=';',
                     thousands='.',
                     decimal=',',
                     )
    return df


def clean_data(df):
    """ Translating the words to english,
    Setting as a pandas dataframe,
     Putting the days in order"""
    df = df.rename(columns={
        'Ativo' : 'Asset',
        'Data' : 'Date',
        'Hora' : 'Time',
        'Abertura' : 'Open',
        'Máximo' : 'High',
        'Mínimo' : 'Low',
        'Fechamento': 'Close',
        'Volume': 'Volume',
        'Quantidade': 'Quantity',
        'Comprador': 'Buyer',
        'Preço' : 'Price',
        'Vendedor' : 'Seller',
        'Tipo' : 'Type'
    })
    df['datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], dayfirst = True)
    df = df.set_index('datetime')
    df = df.sort_index()
    return df


def load_all_files(pattern):
    """Load all the csv files matching pattern"""
    filepaths = glob.glob(pattern)
    dataframes = [clean_data(load_data(fp)) for fp in filepaths]
    combined = pd.concat(dataframes)
    combined = combined.sort_index()
    return combined