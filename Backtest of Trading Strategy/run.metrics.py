import metrics as m
import pandas as pd
df_trades = pd.read_parquet('trades.parquet')

print('='* 40)
print(f'Win rate: {(m.calculate_win_rate('trades.parquet')):.2f}%')
print(f'Profit: {(m.calculate_final_profit('trades.parquet')):.2f} pts')
print('='* 40)
