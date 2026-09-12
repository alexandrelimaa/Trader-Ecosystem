#Risk metrics, everything to understand how bad it could be
from metrics import period_metrics as pm


def accumulated_profit(df):
    """Accumulated Profit = final profit"""
    df = df.sort_values('entry_time').reset_index(drop=True)
    df['accumulated_profit'] = df['profit'].cumsum()
    result= df[['accumulated_profit','entry_time',]]
    return result


def highest_profit(df):
    """Highest Profit ever achieved"""
    df = df.sort_values('entry_time').reset_index(drop=True)
    df['accumulated_profit'] = df['profit'].cumsum()
    df['highest_profit'] = df['accumulated_profit'].cummax()
    result = df['highest_profit'].max()
    return result


def drawdown(df):
    """Lowest profit ever achieved"""
    df = df.sort_values('entry_time').reset_index(drop=True)
    df['accumulated_profit'] = df['profit'].cumsum()
    df['highest_profit'] = df['accumulated_profit'].cummax()
    df['drawdown'] = df['highest_profit'] - df['accumulated_profit']
    result = df[['drawdown', 'entry_time',]]
    return result


def streak_losses(df):
    """Streak losses per trade"""
    df = df.sort_values('entry_time').reset_index(drop=True)
    current_steak = 0
    max_steak = 0
    for index, row in df.iterrows():
        if row['profit'] < 0:
            current_steak += 1
            if current_steak > max_steak:
                max_steak = current_steak
        else:
            current_steak = 0
    return max_steak

def sharpe_ratio(df):
    """Sharpe ratio"""
    profit_series = pm.daily_profit(df)['profit']
    value_average = profit_series.mean()
    value_deviation = profit_series.std()
    result = value_average/value_deviation
    return result

def sortino_ratio(df):
    """Sortino ratio"""
    profit_series = pm.daily_profit(df)['profit']
    value_average = profit_series.mean()
    negative_days = profit_series[profit_series < 0]
    value_deviation = negative_days.std()
    result = value_average / value_deviation
    return result