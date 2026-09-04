import pandas as pd

def calculate_win_rate(fileparquet):
    """Calculate win rate"""
    df = pd.read_parquet(fileparquet)
    win_rate = (df['profit'] > 0).mean() *100
    return win_rate


def calculate_final_profit(fileparquet):
    """Calculate final profit or loss  in WINFUT points"""
    df = pd.read_parquet(fileparquet)
    result = df['profit'].sum()
    return result


def calculate_trades_number(fileparquet):
    """Calculate how many trades were made"""
    df = pd.read_parquet(fileparquet)
    trades_num = len(df)
    return trades_num


def calculate_profit_operations(fileparquet):
    """Calculate how much profit is made in average by trade"""
    df = pd.read_parquet(fileparquet)
    profit_operations = df['profit'].sum() / len(df)
    return profit_operations


def calculate_win_trades_number(fileparquet):
    """Calculate how many trades were a win"""
    df = pd.read_parquet(fileparquet)
    win_trades = (df['profit'] > 0).sum()
    return win_trades


def calculate_loss_trades_number(fileparquet):
    """Calculate how many trades were a loss"""
    df = pd.read_parquet(fileparquet)
    loss_trades = (df['profit'] < 0).sum()
    return loss_trades


def calculate_breakeven(fileparquet):
    """Calculate how many trades were a breakeven"""
    df = pd.read_parquet(fileparquet)
    breakeven = (df['profit'] == 0).sum()
    return breakeven


def calculate_profit_by_time(fileparquet):
    """Calculate profit by time,
    average profit by time,
    number of trade per time,
    win rate by time"""
    df = pd.read_parquet(fileparquet)
    df['time_bucket'] = df['entry_time'].dt.floor(f'{30}min').dt.time
    summary = df.groupby('time_bucket').agg(
        profit=('profit', 'sum'),
        average_profit=('profit', 'mean'),
        number_of_trades=('profit', 'count'),
        win_rate=('profit', lambda x: (x > 0).mean())
    ).reset_index()
    summary['win_rate'] = summary['win_rate'].apply(lambda x: f"{ x * 100:.2f}%")
    summary['average_profit'] = summary['average_profit'].apply(lambda x: f"{ x:.2f} pts")
    summary['profit'] = summary['profit'].apply(lambda x: f"{x:.2f} pts")
    return summary


def calculate_accumulated_profit(fileparquet):
    """Acumulated Profit = final profit"""
    df = pd.read_parquet(fileparquet)
    df['acumulated_profit'] = df['profit'].cumsum()
    acumulated_profit = df['acumulated_profit'].max()
    return acumulated_profit


def calculate_highest_profit(fileparquet):
    """Highest Profit ever achieved"""
    df = pd.read_parquet(fileparquet)
    df['acumulated_profit'] = df['profit'].cumsum()
    df['highest_profit'] = df['acumulated_profit'].cummax()
    highest_profit = df['highest_profit'].max()
    return highest_profit


def calculate_drawdown(fileparquet):
    """Lowest profit ever achieved"""
    df = pd.read_parquet(fileparquet)
    df['acumulated_profit'] = df['profit'].cumsum()
    df['highest_profit'] = df['acumulated_profit'].cummax()
    df['drawdown'] = df['highest_profit'] - df['acumulated_profit']
    drawdown = df['drawdown'].min()
    return drawdown


def calculate_average_time(fileparquet):
    """Average time per trade"""
    df = pd.read_parquet(fileparquet)
    df['duration'] = df['exit_time'] - df['entry_time']
    average_time = df['duration'].mean()
    average_time =f'{average_time.total_seconds() / 60:.2f} min'
    return average_time


def calculate_maximum_time(fileparquet):
    """Maximum time per trade"""
    df = pd.read_parquet(fileparquet)
    df['duration'] = df['exit_time'] - df['entry_time']
    max_time = df['duration'].max()
    max_time = f'{max_time.total_seconds() / 60:.2f} min'
    return max_time


def calculate_minimum_time(fileparquet):
    """Minimum time per trade"""
    df = pd.read_parquet(fileparquet)
    df['duration'] = df['exit_time'] - df['entry_time']
    min_time = df['duration'].min()
    min_time = f'{min_time.total_seconds() / 60:.2f} min'
    return min_time


def calculate_daily_profit(fileparquet):
    """Daily profit of trades"""
    df = pd.read_parquet(fileparquet)
    df['data_bucket'] = df['entry_time'].dt.date
    sum_daily_profit = df.groupby('data_bucket').agg(
        profit=('profit', 'sum')
    ).reset_index()
    return sum_daily_profit

def calculate_weekly_profit(fileparquet):
    """Weekly profit of trades"""
    df = pd.read_parquet(fileparquet)
    df['week_bucket'] = df['entry_time'].dt.to_period('W').dt.start_time
    sum_week_profit = df.groupby('week_bucket').agg(
        profit=('profit', 'sum')
    ).reset_index()
    return sum_week_profit

def calculate_monthly_profit(fileparquet):
    """monthly profit of trades"""
    df = pd.read_parquet(fileparquet)
    df['month_bucket'] = df['entry_time'].dt.to_period('M').dt.start_time
    sum_month_profit = df.groupby('month_bucket').agg(
        profit=('profit', 'sum')
    ).reset_index()
    return sum_month_profit

def calculate_average_number_daily_trades(fileparquet):
    """Average number operations per day"""
    df = pd.read_parquet(fileparquet)
    df['data_bucket'] = df['entry_time'].dt.date
    sum_daily_op = df.groupby('data_bucket').agg(
        number=('profit', 'count')
    ).reset_index()
    return sum_daily_op

def calculate_average_number_week_trades(fileparquet):
    """Average number operations per week"""
    df = pd.read_parquet(fileparquet)
    df['week_bucket'] = df['entry_time'].dt.to_period('W').dt.start_time
    sum_weekly_op = df.groupby('week_bucket').agg(
        number=('profit', 'count')
    ).reset_index()
    return sum_weekly_op

def calculate_average_number_month_trades(fileparquet):
    """Average number operations per month"""
    df = pd.read_parquet(fileparquet)
    df['month_bucket'] = df['entry_time'].dt.to_period('M').dt.start_time
    sum_monthly_op = df.groupby('month_bucket').agg(
        number=('profit', 'count')
    ).reset_index()
    return sum_monthly_op

def calculate_average_daily_profit(fileparquet):
    """Average daily profit of trades"""
    average_dailyprofit = (calculate_daily_profit(fileparquet))['profit'].mean()
    return average_dailyprofit

def calculate_average_weekly_profit(fileparquet):
    """Average weekly profit of trades"""
    average_weeklyprofit = (calculate_weekly_profit(fileparquet))['profit'].mean()
    return average_weeklyprofit

def calculate_average_monthly_profit(fileparquet):
    """Average monthly profit of trades"""
    average_monthlyprofit  = (calculate_monthly_profit(fileparquet))['profit'].mean()
    return average_monthlyprofit