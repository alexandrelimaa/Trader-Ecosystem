#Libraries
import pandas as pd
import numpy as np
import helpers as h
from datetime import time

#==== Strategy Paraments ====
short_ema = 9
long_ema = 400
timeframe = '3min'
session_start = time(9 , 40)
session_end = time(11 , 15)
stop_loss = 200
trailing_activation = 65
trailing_stop = 15

#=====================================
#Cleaning the data:
candle_1min = h.clean_data(h.load_data("dados/WINFUT2026-08-01(1min).csv"))
tick_data = h.load_all_files('dados/tick_*.csv')

#=================================

candle = candle_1min.resample(timeframe).agg({
    'Abertura' : 'first',
    'Fechamento' : 'last',
    'Volume' : 'sum',
    'Máximo' : 'max',
    'Mínimo' : 'min'
})

#Creating EMA's
candle['short_ema'] = candle['Fechamento'].ewm(span=short_ema, adjust=False).mean()
candle['long_ema'] = candle['Fechamento'].ewm(span=long_ema, adjust=False).mean()

#Creating entry signal
condition = [
    candle['Fechamento'] > candle['long_ema'],
    candle['Fechamento'] < candle['long_ema'],
    candle['Fechamento'] == candle['long_ema'],
]
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
candle['touched_short_ema'] = np.select(condition2, results2)
#Next Candle
candle['closed_direction'] = np.where(candle['trend'] == 'up',
                          candle['Fechamento'] > candle['Abertura'], candle['Fechamento'] < candle['Abertura'])
candle['touched_previous'] = candle['touched_short_ema'].shift(1)

#Montar o limite de horario
candle['within_session'] = (candle.index.time >= session_start) & (candle.index.time <= session_end)
candle['next_within_session'] = candle['within_session'].shift(-1)

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

#Aplicar loop de entrada

# Variavéis simples
position_open = False
trade_type = None          #buy or sell
entry_price =None
candle['buy_sell_price'] = candle['Abertura'].shift(-1)
exit_price = None
best_price = None           #preço mais favoravél desde o começo
trailing_active = False
current_stoploss = None
last_exit_time = None
profit = None
trades = []                   # saving trades

#Loop
warmup_start = tick_data.index.min()
for index, candle_row in candle.loc[warmup_start:].iterrows():

    if not position_open:
        if last_exit_time is not None and index <= last_exit_time:
            continue

        if candle_row['buy_signal']:
            position_open = True
            trade_type = 'buy'
            entry_price = candle_row['buy_sell_price']
            current_stoploss = entry_price - stop_loss
            best_price = entry_price

        elif candle_row['sell_signal']:
            position_open = True
            trade_type = 'sell'
            entry_price = candle_row['buy_sell_price']
            current_stoploss = entry_price + stop_loss
            best_price = entry_price

    if position_open:
        execution_time = index +pd.Timedelta(timeframe)
        operation_ticks = tick_data.loc[execution_time:]
        for index_tick, tick in operation_ticks.iterrows():
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
df_trades = pd.DataFrame(trades)
print(len(df_trades))
print(df_trades.head())