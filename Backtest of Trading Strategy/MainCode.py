#Libraries
import pandas as pd
import numpy as np
import helpers as h
from datetime import time

#==== Strategy Paraments ====#
    #---TimeFrame--#
timeframe = '3min'
    #---Exponecial Moving Average---#
short_ema = 9
long_ema = 400
    #---Time of Operation---#
session_start = time(9 , 40)          #Only for entrance
session_end = time(11 , 15)
    #---Stop Loss and Take Profit---#
stop_loss = 200
trailing_activation = 65   #whenever hits 65 points = 13 tick
trailing_stop = 15         #protect with 3 ticks of distance after ativacion
#===========================#

#=== Organizing files ===#
candle_1min = h.clean_data(h.load_data("dados/WINFUT2026-08-01(1min).csv"))     #candle in 1min
tick_data = h.load_all_files('dados/tick_*.csv')            #trade by trade in the period
candle = candle_1min.resample(timeframe).agg({
    'Abertura' : 'first',
    'Fechamento' : 'last',
    'Volume' : 'sum',
    'Máximo' : 'max',
    'Mínimo' : 'min'
})    # whatever timeframe you choose
#========================#

#=== Creating EMA's ===#
candle['short_ema'] = candle['Fechamento'].ewm(span=short_ema, adjust=False).mean()
candle['long_ema'] = candle['Fechamento'].ewm(span=long_ema, adjust=False).mean()
#=====================#

#=== Creating entry signal ===#
condition = [
    candle['Fechamento'] > candle['long_ema'],
    candle['Fechamento'] < candle['long_ema'],
    candle['Fechamento'] == candle['long_ema'],
]      #filter in the candles, following the big trend
results = [
    'up',
    'down',
    'neutral'
]
candle['trend'] = np.select(condition, results, default = 'undefined')
condition2 = [
    candle['trend'] == 'up',
    candle['trend'] == 'down',
    candle['trend'] == 'neutral'
]
results2 = [
    (candle['Mínimo'] <= candle['short_ema']) & (candle['short_ema'] <= candle['Máximo']),
    (candle['Máximo'] >= candle['short_ema']) & (candle['short_ema'] >= candle['Mínimo']),
    False
]
candle['touched_short_ema'] = np.select(condition2, results2)   #touch the short ema
candle['closed_direction'] = np.where(candle['trend'] == 'up',
                          candle['Fechamento'] > candle['Abertura'], candle['Fechamento'] < candle['Abertura'])
candle['touched_previous'] = candle['touched_short_ema'].shift(1)
    # if the candle who did touched the ema close to the wrong direction, if the next one goes to the right direction it also counts

candle['within_session'] = (candle.index.time >= session_start) & (candle.index.time <= session_end)
candle['next_within_session'] = candle['within_session'].shift(-1)
    #time limitation
    #--- Checking if the signal was real ---#
candle['buy_signal'] =(
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
candle['sell_signal'] =(
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
#=============================#

#=== Simulation Loop ===#

    #--- Stable Variables ---#
position_open = False
trade_type = None          #buy or sell
entry_price =None
candle['buy_sell_price'] = candle['Abertura'].shift(-1)
exit_price = None
best_price = None           #the most favorable price until the moment
trailing_active = False
current_stoploss = None     #always following the best_price by 3 ticks of distance
last_exit_time = None
profit = None
trades = []                   # saving trades in a list

    #--- Simulation Loop Machine ---#
warmup_start = tick_data.index.min()
for index, candle_row in candle.loc[warmup_start:].iterrows():
    #while position not opened yet
    if not position_open:
        if last_exit_time is not None and index <= last_exit_time:
            continue
        #if it's buy
        if candle_row['buy_signal']:
            position_open = True
            trade_type = 'buy'
            entry_price = candle_row['buy_sell_price']
            current_stoploss = entry_price - stop_loss
            best_price = entry_price
        #if it's sell
        elif candle_row['sell_signal']:
            position_open = True
            trade_type = 'sell'
            entry_price = candle_row['buy_sell_price']
            current_stoploss = entry_price + stop_loss
            best_price = entry_price
    #inding the exit
    if position_open:
        execution_time = index +pd.Timedelta(timeframe)
        operation_ticks = tick_data.loc[execution_time:]
        for index_tick, tick in operation_ticks.iterrows():
            #if was a buy
            if trade_type == 'buy':
                if  best_price < tick['Preço']:
                    best_price = tick['Preço']
                    if best_price >= (entry_price + trailing_activation):
                        trailing_active = True
                        current_stoploss = ( best_price - trailing_stop )
                if tick['Preço'] <= current_stoploss:
                    trailing_active = False
                    exit_price = tick['Preço']
                    profit = exit_price - entry_price
                    trades.append({
                        'trade_type' : trade_type,
                        'entry_price' : entry_price,
                        'exit_price' : exit_price,
                        'profit' : profit,
                        'entry_time' : index,
                        'exit_time' : index_tick,
                    })
                    last_exit_time = index_tick
                    position_open = False
                    break
            #if was a sell
            if trade_type == 'sell':
                if best_price > tick['Preço']:
                    best_price = tick['Preço']
                    if best_price <= (entry_price - trailing_activation) :
                        trailing_active = True
                        current_stoploss = ( best_price + trailing_stop )
                if tick['Preço'] >= current_stoploss:
                    trailing_active = False
                    exit_price = tick['Preço']
                    profit = entry_price - exit_price
                    trades.append({
                        'trade_type': trade_type,
                        'entry_price': entry_price,
                        'exit_price': exit_price,
                        'profit': profit,
                        'entry_time': index,
                        'exit_time': index_tick,
                    })
                    last_exit_time = index_tick
                    position_open = False
                    break
#======================#

#=== Making the list ===#
df_trades = pd.DataFrame(trades)
print(len(df_trades))
print(df_trades.head())
#=======================#