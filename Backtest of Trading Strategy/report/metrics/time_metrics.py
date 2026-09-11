#Time metrics, how long a trade should take

def average_time(df):
    """Average time per trade"""
    df = df.copy()
    df['duration'] = df['exit_time'] - df['entry_time']
    result = df['duration'].mean()
    return result

def maximum_time(df):
    df = df.copy()
    """Maximum time per trade"""
    df['duration'] = df['exit_time'] - df['entry_time']
    result = df['duration'].max()
    return result


def minimum_time(df):
    """Minimum time per trade"""
    df = df.copy()
    df['duration'] = df['exit_time'] - df['entry_time']
    result = df['duration'].min()
    return result
