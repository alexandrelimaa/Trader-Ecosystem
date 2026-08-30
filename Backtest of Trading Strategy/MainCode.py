#Bibliotecas
import pandas as pd
import numpy as np
from datetime import time

#limpando os dados:
ummin = pd.read_csv("dados/WINFUT2026-08-01(1min).csv",
                    encoding = 'latin1',
                    sep = ';',
                    thousands='.',
                    decimal = ','
                    )
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
candle_3min = ummin.resample('3min') .agg({
    'Abertura' : 'first',
    'Fechamento' : 'last',
    'Volume' : 'sum',
    'Máximo' : 'max',
    'Mínimo' : 'min'
})

#Criando as EMA
candle_3min['ema9'] = candle_3min['Fechamento'].ewm(span=9, adjust=False).mean()
candle_3min['ema400'] = candle_3min['Fechamento'].ewm(span=400, adjust=False).mean()
#print(candle_3min[['Fechamento', 'ema9', 'ema400']].head(10))

#Criando entrada
condicao = [
    candle_3min['Fechamento'] > candle_3min['ema400'],
    candle_3min['Fechamento'] < candle_3min['ema400'],
    candle_3min['Fechamento'] == candle_3min['ema400'],
]
resultados = [
    'alta',
    'baixa',
    'neutro'
]
candle_3min['tendencia'] = np.select(condicao, resultados, default = 'indefinido')
condicao2 = [
    candle_3min['tendencia'] == 'alta',
    candle_3min['tendencia'] == 'baixa',
    candle_3min['tendencia'] == 'neutro'
]
resultados2 = [
    (candle_3min['Mínimo'] <= candle_3min['ema9']) & (candle_3min['ema9'] <= candle_3min['Máximo']),
    (candle_3min['Máximo'] >= candle_3min['ema9']) & (candle_3min['ema9'] >= candle_3min['Mínimo']),
    False
]
candle_3min['tocou_ema9'] = np.select(condicao2, resultados2)
#Proximo Candle
candle_3min['fechou_direcao'] = np.where(candle_3min['tendencia'] == 'alta',
                          candle_3min['Fechamento'] > candle_3min['Abertura'], candle_3min['Fechamento'] < candle_3min['Abertura'])
candle_3min['tocou_anterior'] = candle_3min['tocou_ema9'].shift(1)

#Montar o limite de horario
candle_3min['dentro_horario'] = (candle_3min.index.time >= time(9,40)) & (candle_3min.index.time <= time(11,15))
#11:18 não entra
candle_3min['seguinte_dentro_hora'] = candle_3min['dentro_horario'].shift(-1)

candle_3min['sinal_compra'] =(
    ((candle_3min['tendencia'] == 'alta') &
    (candle_3min['fechou_direcao'] == True) &
    (candle_3min['tocou_ema9'] == True) &
    (candle_3min['dentro_horario'] == True) &
    (candle_3min['seguinte_dentro_hora'] == True)) |
    ((candle_3min['tendencia'] == 'alta') &
    (candle_3min['fechou_direcao'] == True) &
    (candle_3min['tocou_anterior'] == True) &
    (candle_3min['dentro_horario'] == True) &
    (candle_3min['seguinte_dentro_hora'] == True))
)
candle_3min['sinal_venda'] =(
    ((candle_3min['tendencia'] == 'baixa') &
    (candle_3min['fechou_direcao'] == True) &
    (candle_3min['tocou_ema9'] == True) &
    (candle_3min['dentro_horario'] == True) &
    (candle_3min['seguinte_dentro_hora'] == True)) |
    ((candle_3min['tendencia'] == 'baixa') &
    (candle_3min['fechou_direcao'] == True) &
    (candle_3min['tocou_anterior'] == True) &
    (candle_3min['dentro_horario'] == True) &
    (candle_3min['seguinte_dentro_hora'] == True))
)

#Aplicar loop de entrada

# Variavéis simples
posicao_aberta = False
tipo_operacao = None          #compra ou venda
candle_3min['preco_entrada_compra_venda'] = candle_3min['Abertura'].shift(-1)
preco_entrada = None
preco_saida = None
melhor_preco = None           #preço mais favoravél desde o começo
trailing_ativo = False
stop_atual = None
horario_saida_anterior = None
lucro = None
trades = []                   # guardar os trades feitos

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
#Métricas
df_trades = pd.DataFrame(trades)
#Win rate
win_rate = ((df_trades['lucro'] > 0).mean()) * 100
print(f'Win Rate: {win_rate:.2f}%')
#Gain e Loss médio
gain_medio = df_trades[df_trades['lucro'] > 0]['lucro'].mean()
print(f'Gain Médio: {gain_medio:.2f}')
loss_medio = df_trades[df_trades['lucro'] < 0]['lucro'].mean()
print(f'Loss Médio: {loss_medio:.2f}')

