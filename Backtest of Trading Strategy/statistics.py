#def para maincode
import numpy as np

from MainCode import best_price, current_stop_loss


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
        trailing_on = best_price >= (entry_price +trailing_activation)
        current_stop_loss = np.where(trailing_on , best_price - trailing_stop, entry_price - stop_loss)
        exit_condition = tick_after_entry['Price'] <= current_stop_loss
        exit_time = exit_condition.idxmax()
        exit_price = tick_after_entry.loc[exit_time, 'Price']

    elif trade_type == 'sell':
        best_price = tick_after_entry['Price'].cummin()
        trailing_on = best_price <= (entry_price + trailing_activation)
        current_stop_loss = np.where(trailing_on, best_price + trailing_stop, entry_price + stop_loss)
        exit_condition = tick_after_entry['Price'] >= current_stop_loss
        exit_time = exit_condition.idxmax()
        exit_price = tick_after_entry.loc[exit_time, 'Price']