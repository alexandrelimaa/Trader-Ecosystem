#Profit Metrics, all the metrics about result and efficiency

def win_rate(df):
    """Calculate win rate"""
    result = (df['profit'] > 0).mean() *100
    return result

def final_profit(df):
    """Calculate final profit or loss  in WINFUT points"""
    result = df['profit'].sum()
    return result

def trades_number(df):
    """Calculate how many trades were made"""
    result = len(df)
    return result

def profit_per_operations(df):
    """Calculate how much profit is made in average by trade"""
    result = df['profit'].sum() / len(df)
    return result

def win_trades_number(df):
    """Calculate how many trades were a win"""
    result = (df['profit'] > 0).sum()
    return result

def loss_trades_number(df):
    """Calculate how many trades were a loss"""
    result = (df['profit'] < 0).sum()
    return result

def breakeven(df):
    """Calculate how many trades were a breakeven"""
    result = (df['profit'] == 0).sum()
    return result

def sum_win_trades(df):
    """Sum win trades"""
    result = df[df['profit'] > 0]['profit'].sum()
    return result

def sum_loss_trades(df):
    """Sum loss trades"""
    result = df[df['profit'] < 0]['profit'].sum()
    result = result * - 1
    return result

def profit_factor(df):
    """Profit factor"""
    sum_win =  sum_win_trades(df)
    sum_loss = sum_loss_trades(df)
    result = sum_win / sum_loss
    return result if sum_loss != 0 else None

def expectancy_factor(df):
    """Expectancy factor"""
    average_gain = df[df['profit'] > 0]['profit'].mean()
    winrate = win_rate(df)/100
    win_side = winrate * average_gain
    loss_rate = 100 - win_rate(df)
    loss_rate = loss_rate / 100
    average_loss = df[df['profit'] < 0]['profit'].mean()
    average_loss = average_loss * - 1
    loss_side = loss_rate * average_loss
    result = win_side - loss_side
    return result
