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
    )
    summary['win_rate'] = summary['win_rate'].apply(lambda x: f"{ x * 100:.2f}%")
    summary['average_profit'] = summary['average_profit'].apply(lambda x: f"{ x:.2f} pts")
    summary['profit'] = summary['profit'].apply(lambda x: f"{x:.2f} pts")
    return summary


def calculate_acumulated_profit(fileparquet):
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


# Tempo medio por op
#Media Diaria
#qtd op dia e semanal
# Media diaria de gain
#Media diaria de loss
#Media semanal