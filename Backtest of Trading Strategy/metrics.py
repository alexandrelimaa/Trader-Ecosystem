import pandas as pd

def calculate_win_rate(fileparquet):
    df = pd.read_parquet(fileparquet)
    win_rate = (df['profit'] > 0).mean() *100
    return win_rate


def calculate_trades_number(fileparquet):
    df = pd.read_parquet(fileparquet)
    result = df['profit'].sum()
    return result                          #Result of all trades
#trades_num = len(df_trades)              #quantity of trades it toke
#profit_operation = result / trades_num   #average profit per trade
#win_trades = (df_trades['profit'] > 0).sum()
#loss_trades = (df_trades['profit'] <= 0).sum()
#Lucro por Horario
#Drawndown max
# Tempo medio por op
#Media Diaria
#qtd op dia e semanal
# Media diaria de gain
#Media diaria de loss
#Media semanal
