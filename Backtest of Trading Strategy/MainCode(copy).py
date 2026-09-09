#Libraries
import pandas as pd
import numpy as np
import helpers as h
from datetime import time
import statistics as st
from statistics import calculate_emas

#==== Strategy Paraments ====#
    #---TimeFrame--#
timeframe = '3min'
    #---Exponential Moving Average---#
short_ema = 9
long_ema = 400
    #---Time of Operation---#
session_start = time(9 , 40)          #Only for entrance
session_end = time(11 , 15)
    #---Stop Loss and Take Profit---#
stop_loss = 200
trailing_activation = 65   #whenever hits 65 points = 13 tick
trailing_stop = 15         #protect with 3 ticks of distance after activation
    #---Data for the backtest---#
candle_files_pattern = "Files/Minutes of WINFUT/candle_*.csv"
tick_files_pattern = "Files/Ticks of WINFUT/tick_*.csv"
#===========================#

#=== Organizing files ===#
candle_1min = h.load_all_files(candle_files_pattern)   #candle in 1min
tick_data = h.load_all_files(tick_files_pattern)            #trade by trade in the period
candle = candle_1min.resample(timeframe).agg({
    'Open' : 'first',
    'Close' : 'last',
    'Volume' : 'sum',
    'High' : 'max',
    'Low' : 'min'
})    # whatever timeframe you choose
#========================#

#=== Creating EMA's ===#
candle = st.calculate_emas(candle,short_ema,long_ema)

#=====================#

#=== Creating entry signal ===#
candle = st.calculate_signal(candle, session_start, session_end)

#=============================#

#===Transaction Cost ===#
cost_per_trade = 10

#=== Simulation Loop ===#

    #--- Stable Variables ---#
position_open = False
trade_type = None          #buy or sell
entry_price =None
candle['buy_sell_price'] = candle['Open'].shift(-1)
exit_price = None
best_price = None           #the most favorable price until the moment
trailing_active = False
current_stop_loss = None     #always following the best_price by 3 ticks of distance
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
            current_stop_loss = entry_price - stop_loss
            best_price = entry_price
        #if it's sell
        elif candle_row['sell_signal']:
            position_open = True
            trade_type = 'sell'
            entry_price = candle_row['buy_sell_price']
            current_stop_loss = entry_price + stop_loss
            best_price = entry_price
    #finding the exit

    
    if position_open:
        execution_time = index +pd.Timedelta(timeframe)
        operation_ticks = tick_data.loc[execution_time:]
        for index_tick, tick in operation_ticks.iterrows():
            #if was a buy
            if trade_type == 'buy':
                if  best_price < tick['Price']:
                    best_price = tick['Price']
                    if best_price >= (entry_price + trailing_activation):
                        trailing_active = True
                        current_stop_loss = ( best_price - trailing_stop )
                if tick['Price'] <= current_stop_loss:
                    trailing_active = False
                    exit_price = tick['Price']
                    profit = (exit_price - entry_price) - cost_per_trade
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
                if best_price > tick['Price']:
                    best_price = tick['Price']
                    if best_price <= (entry_price - trailing_activation) :
                        trailing_active = True
                        current_stop_loss = ( best_price + trailing_stop )
                if tick['Price'] >= current_stop_loss:
                    trailing_active = False
                    exit_price = tick['Price']
                    profit = (entry_price - exit_price) - cost_per_trade
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
df_trades.to_parquet('trades.parquet(1)')    # Salve the file to use in metrics
#=======================#