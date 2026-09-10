#Libraries
import pandas as pd
import numpy as np
import helpers as h
from datetime import time
import strategy as st

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

    #--- Cost per Trade---#
cost_per_trade = 10
    #--- Asset ---#
asset = 'WINFUT'

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
candle['buy_sell_price'] = candle['Open'].shift(-1)
#=============================#

#=== Simulation Loop ===#
df_trades = st.run_simulation(candle, tick_data, stop_loss, trailing_activation, trailing_stop, timeframe, cost_per_trade, asset)
#======================#

#=== Making the list ===#
df_trades.to_parquet('trades.parquet(1copy)')    # Salve the file to use in metrics
#=======================#