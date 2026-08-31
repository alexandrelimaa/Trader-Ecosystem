#Libraries
import pandas as pd
import numpy as np
import helpers as h
from datetime import time

#==== Strategy Paraments ====
short_ema = 9
long_ema = 400
timeframe = 3
session_start = time(9 , 40)
session_end = time(11 , 15)
stop_loss = 200
trailing_activation = 65
trailing_stop = 15

#=====================================
#Cleaning the data:
candle_1min = h.clean_data(h.load_data("dados/WINFUT2026-08-01(1min).csv"))
#ummin = pd.read_csv("dados/WINFUT2026-08-01(1min).csv",
                   # encoding = 'latin1',
                    #sep = ';',
                    #thousands='.',
                    #decimal = ','
                   # )
tick_11 = pd.read_csv("dados/2026-08-11a18 tick a tick.csv",
                      encoding='latin1', sep=';', thousands='.', decimal=',')
tick_12 = pd.read_csv('dados/tick_12_08.csv',
                      encoding='latin1', sep=';', thousands='.', decimal=',')
# ... um pra cada dia

tickatick = pd.concat([tick_11, tick_12], ignore_index=True)
    #Unificando data e hora

ummin['datetime']= pd.to_datetime(ummin['Data'] + ' ' + ummin['Hora'], dayfirst = True)
tickatick['datetime']= pd.to_datetime(tickatick['Data']+ ' '+ tickatick['Hora'], dayfirst = True)
#criando o candle de 3min

tickatick = tickatick.set_index('datetime')
tickatick = tickatick.sort_index()
ummin = ummin.set_index('datetime')


#=================================
#fazer um for para juntar os candle no timeframe que quero
candle_3min = ummin.resample('3min') .agg({
    'Abertura' : 'first',
    'Fechamento' : 'last',
    'Volume' : 'sum',
    'Máximo' : 'max',
    'Mínimo' : 'min'
})

#Creating EMA's
#modificar o nome candle_3min
candle_3min['short_ema'] = candle_3min['Fechamento'].ewm(span=short_ema, adjust=False).mean()
candle_3min['long_ema'] = candle_3min['Fechamento'].ewm(span=long_ema, adjust=False).mean()

#Creating entry signal
condition = [
    candle_3min['Fechamento'] > candle_3min['long_ema'],
    candle_3min['Fechamento'] < candle_3min['long_ema'],
    candle_3min['Fechamento'] == candle_3min['long_ema'],
]
results = [
    'up',
    'down',
    'neutral'
]
candle_3min['trend'] = np.select(condition, results, default = 'undefined')
condition2 = [
    candle_3min['trend'] == 'up',
    candle_3min['trend'] == 'down',
    candle_3min['trend'] == 'neutral'
]
results2 = [
    (candle_3min['Mínimo'] <= candle_3min['short_ema']) & (candle_3min['short_ema'] <= candle_3min['Máximo']),
    (candle_3min['Máximo'] >= candle_3min['short_ema']) & (candle_3min['short_ema'] >= candle_3min['Mínimo']),
    False
]
candle_3min['touched_short_ema'] = np.select(condition2, results2)
#Next Candle
candle_3min['closed_direction'] = np.where(candle_3min['trend'] == 'up',
                          candle_3min['Fechamento'] > candle_3min['Abertura'], candle_3min['Fechamento'] < candle_3min['Abertura'])
candle_3min['touched_previous'] = candle_3min['touched_short_ema'].shift(1)

#Montar o limite de horario
candle_3min['within_session'] = (candle_3min.index.time >= time(session_start)) & (candle_3min.index.time <= time(session_end))
#11:18 não entra
candle_3min['next_within_session'] = candle_3min['within_session'].shift(-1)

candle_3min['buy_signal'] =(
    ((candle_3min['trend'] == 'up') &
    (candle_3min['closed_direction'] == True) &
    (candle_3min['touched_short_ema'] == True) &
    (candle_3min['within_session'] == True) &
    (candle_3min['next_within_session'] == True)) |
    ((candle_3min['trend'] == 'alta') &
    (candle_3min['closed_direction'] == True) &
    (candle_3min['touched_previous'] == True) &
    (candle_3min['within_session'] == True) &
    (candle_3min['next_within_session'] == True))
)
candle_3min['sell_signal'] =(
    ((candle_3min['trend'] == 'down') &
    (candle_3min['closed_direction'] == True) &
    (candle_3min['touched_short_ema'] == True) &
    (candle_3min['within_session'] == True) &
    (candle_3min['next_within_session'] == True)) |
    ((candle_3min['trend'] == 'down') &
    (candle_3min['closed_direction'] == True) &
    (candle_3min['touched_previous'] == True) &
    (candle_3min['within_session'] == True) &
    (candle_3min['next_within_session'] == True))
)

#Aplicar loop de entrada

# Variavéis simples
open_position = False
trade_type = None          #buy or sell
entry_price = candle_3min['Abertura'].shift(-1)
exit_price = None
best_price = None           #preço mais favoravél desde o começo
trailing_active = False
current_stoploss = None
last_exit_time = None
profit = None
trades = []                   # saving trades

#Loop
inicio_tick = tickatick.index.min()
for index, candle in candle_3min.loc[inicio_tick:].iterrows():
    if not posicao_aberta:

        if horario_saida_anterior is not None and index <= horario_saida_anterior:
            continue
        if candle['sinal_compra']:
            posicao_aberta = True
            tipo_operacao = 'compra'
            preco_entrada =  candle['preco_entrada_compra_venda']
            stop_atual = preco_entrada - 200
            melhor_preco = preco_entrada

        elif candle['sinal_venda']:
            posicao_aberta = True
            tipo_operacao = 'venda'
            preco_entrada = candle['preco_entrada_compra_venda']
            stop_atual = preco_entrada + 200
            melhor_preco= preco_entrada
    if posicao_aberta:
        index_execucao = index +pd.Timedelta(minutes = 3)
        ticks_da_operacao = tickatick.loc[index_execucao:]
        for index_tick, tick in ticks_da_operacao.iterrows():
            if tipo_operacao == 'compra':
                if  melhor_preco < tick['Preço']:
                    melhor_preco = tick['Preço']
                    if melhor_preco >= (preco_entrada + 65):
                        trailing_ativo = True
                        stop_atual = ( melhor_preco - 15 )
                if tick['Preço'] <= stop_atual:
                    trailing_ativo = False
                    preco_saida = tick['Preço']
                    lucro = preco_saida - preco_entrada
                    trades.append({
                        'tipo' : tipo_operacao,
                        'preco_entrada' : preco_entrada,
                        'preco_saida' : preco_saida,
                        'lucro' : lucro,
                        'hora_entrada' : index,
                        'hora_saida' : index_tick,
                    })
                    horario_saida_anterior = index_tick
                    posicao_aberta = False

                    break
            if tipo_operacao == 'venda':
                if melhor_preco > tick['Preço']:
                    melhor_preco = tick['Preço']
                    if melhor_preco <= (preco_entrada - 65) :
                        trailing_ativo = True
                        stop_atual = ( melhor_preco + 15 )
                if tick['Preço'] >= stop_atual:
                    trailing_ativo = False
                    preco_saida = tick['Preço']
                    lucro = preco_entrada - preco_saida
                    trades.append({
                        'tipo': tipo_operacao,
                        'preco_entrada': preco_entrada,
                        'preco_saida': preco_saida,
                        'lucro': lucro,
                        'hora_entrada': index,
                        'hora_saida': index_tick,
                    })
                    horario_saida_anterior = index_tick
                    posicao_aberta = False
                    break
df_trades = pd.DataFrame(trades)