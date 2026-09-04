#Period Metrics, what happens in a period of time,
# What should I expect of the market in this period

def profit_by_time(df):
    """Calculate profit by time,
    average profit by time,
    number of trade per time,
    win rate by time"""
    df = df.copy()
    df['time_bucket'] = df['entry_time'].dt.floor(f'{30}min').dt.time
    summary = df.groupby('time_bucket').agg(
        profit=('profit', 'sum'),
        average_profit=('profit', 'mean'),
        number_of_trades=('profit', 'count'),
        win_rate=('profit', lambda x: (x > 0).mean())
    ).reset_index()
    return summary

def daily_profit(df):
    """Daily profit of trades"""
    df = df.copy()
    df['data_bucket'] = df['entry_time'].dt.date
    result = df.groupby('data_bucket').agg(
        profit=('profit', 'sum')
    ).reset_index()
    return result

def weekly_profit(df):
    """Weekly profit of trades"""
    df = df.copy()
    df['week_bucket'] = df['entry_time'].dt.to_period('W').dt.start_time
    result = df.groupby('week_bucket').agg(
        profit=('profit', 'sum')
    ).reset_index()
    return result

def monthly_profit(df):
    """monthly profit of trades"""
    df = df.copy()
    df['month_bucket'] = df['entry_time'].dt.to_period('M').dt.start_time
    result = df.groupby('month_bucket').agg(
        profit=('profit', 'sum')
    ).reset_index()
    return result

def average_number_daily_trades(df):
    """Average number operations per day"""
    df = df.copy()
    df['data_bucket'] = df['entry_time'].dt.date
    result = df.groupby('data_bucket').agg(
        number=('profit', 'count')
    ).reset_index()
    return result

def average_number_week_trades(df):
    """Average number operations per week"""
    df = df.copy()
    df['week_bucket'] = df['entry_time'].dt.to_period('W').dt.start_time
    result = df.groupby('week_bucket').agg(
        number=('profit', 'count')
    ).reset_index()
    return result

def average_number_month_trades(df):
    """Average number operations per month"""
    df = df.copy()
    df['month_bucket'] = df['entry_time'].dt.to_period('M').dt.start_time
    result = df.groupby('month_bucket').agg(
        number=('profit', 'count')
    ).reset_index()
    return result

def average_daily_profit(df):
    """Average daily profit of trades"""
    result = (daily_profit(df))['profit'].mean()
    return result

def average_weekly_profit(df):
    """Average weekly profit of trades"""
    result = (weekly_profit(df))['profit'].mean()
    return result

def average_monthly_profit(df):
    """Average monthly profit of trades"""
    result  = (monthly_profit(df))['profit'].mean()
    return result