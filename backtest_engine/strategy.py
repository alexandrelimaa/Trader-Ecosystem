#def para maincode
import numpy as np
import pandas as pd

def calculate_emas(candle,short_period,long_period):
    candle['short_ema'] = candle['Close'].ewm(span=short_period, adjust=False).mean()
    candle['long_ema'] = candle['Close'].ewm(span=long_period, adjust=False).mean()
    return candle


def calculate_signal(candle,session_start,session_end):
    """Create and calculate signal for candle"""
    # === Creating entry signal ===#
    condition = [
        candle['Close'] > candle['long_ema'],
        candle['Close'] < candle['long_ema'],
        candle['Close'] == candle['long_ema'],
    ]  # filter in the candles, following the big trend
    results = [
        'up',
        'down',
        'neutral'
    ]
    candle['trend'] = np.select(condition, results, default='undefined')
    condition2 = [
        candle['trend'] == 'up',
        candle['trend'] == 'down',
        candle['trend'] == 'neutral'
    ]
    results2 = [
        (candle['Low'] <= candle['short_ema']) & (candle['short_ema'] <= candle['High']),
        (candle['High'] >= candle['short_ema']) & (candle['short_ema'] >= candle['Low']),
        False
    ]
    candle['touched_short_ema'] = np.select(condition2, results2)  # touch the short ema
    candle['closed_direction'] = np.where(candle['trend'] == 'up',
                                          candle['Close'] > candle['Open'], candle['Close'] < candle['Open'])
    candle['touched_previous'] = candle['touched_short_ema'].shift(1)
    # if the candle who did touch the ema close to the wrong direction, if the next one goes to the right direction it also counts

    candle['within_session'] = (candle.index.time >= session_start) & (candle.index.time <= session_end)
    candle['next_within_session'] = candle['within_session'].shift(-1)
    # time limitation
    # --- Checking if the signal was real ---#
    candle['buy_signal'] = (
            ((candle['trend'] == 'up') &
             (candle['closed_direction'] == True) &
             (candle['touched_short_ema'] == True) &
             (candle['within_session'] == True) &
             (candle['next_within_session'] == True)) |
            ((candle['trend'] == 'up') &
             (candle['closed_direction'] == True) &
             (candle['touched_previous'] == True) &
             (candle['within_session'] == True) &
             (candle['next_within_session'] == True))
    )
    candle['sell_signal'] = (
            ((candle['trend'] == 'down') &
             (candle['closed_direction'] == True) &
             (candle['touched_short_ema'] == True) &
             (candle['within_session'] == True) &
             (candle['next_within_session'] == True)) |
            ((candle['trend'] == 'down') &
             (candle['closed_direction'] == True) &
             (candle['touched_previous'] == True) &
             (candle['within_session'] == True) &
             (candle['next_within_session'] == True))
    )
    return candle

def simulate_tick(entry_price, trade_type, tick_after_entry, stop_loss, trailing_activation, trailing_stop):


    if trade_type == 'buy':
        best_price = tick_after_entry['Price'].cummax()
        trailing_on = best_price >= (entry_price + trailing_activation)
        current_stop_loss = np.where(trailing_on , best_price - trailing_stop, entry_price - stop_loss)
        exit_condition = tick_after_entry['Price'] <= current_stop_loss
        if not exit_condition.any():
            return None, None
        exit_position = exit_condition.values.argmax()
        exit_price = tick_after_entry['Price'].iloc[exit_position]
        exit_time = tick_after_entry.index[exit_position]
        return exit_time, exit_price

    elif trade_type == 'sell':
        best_price = tick_after_entry['Price'].cummin()
        trailing_on = best_price <= (entry_price - trailing_activation)
        current_stop_loss = np.where(trailing_on, best_price + trailing_stop, entry_price + stop_loss)
        exit_condition = tick_after_entry['Price'] >= current_stop_loss
        if not exit_condition.any():
            return None, None
        exit_position = exit_condition.values.argmax()
        exit_price = tick_after_entry['Price'].iloc[exit_position]
        exit_time = tick_after_entry.index[exit_position]
        return exit_time, exit_price



def run_simulation(candle, tick_data, stop_loss, trailing_activation, trailing_stop, timeframe, cost_per_trade, asset):
    position_open = False
    last_exit_time = None
    trades = []
    warmup_start = tick_data.index.min()
    for index, candle_row in candle.loc[warmup_start:].iterrows():
        signal_found = False
        # while position not opened yet
        if not position_open:
            if last_exit_time is not None and index <= last_exit_time:
                continue
            # if it's buy
            if candle_row['buy_signal']:
                position_open = True
                trade_type = 'buy'
                entry_price = candle_row['buy_sell_price']
                execution_time = index + pd.Timedelta(timeframe)
                operation_ticks = tick_data.loc[execution_time:]
                signal_found = True
            # if it's sell
            elif candle_row['sell_signal']:
                position_open = True
                trade_type = 'sell'
                entry_price = candle_row['buy_sell_price']
                execution_time = index + pd.Timedelta(timeframe)
                operation_ticks = tick_data.loc[execution_time:]
                signal_found = True
            if signal_found:
                exit_time, exit_price = simulate_tick( entry_price, trade_type, operation_ticks, stop_loss,trailing_activation, trailing_stop)
                if exit_time is not None:
                    if trade_type == 'buy':
                        profit = (entry_price - exit_price) - cost_per_trade
                    elif trade_type == 'sell':
                        profit = (exit_price - entry_price) - cost_per_trade
                    trades.append({
                        'asset' : asset,
                        'trade_type': trade_type,
                        'entry_price': entry_price,
                        'exit_price': exit_price,
                        'profit': profit,
                        'entry_time': index,
                        'exit_time': exit_time
                    })
                    last_exit_time = exit_time
                    position_open = False
                else:
                    position_open = False
    return pd.DataFrame(trades)