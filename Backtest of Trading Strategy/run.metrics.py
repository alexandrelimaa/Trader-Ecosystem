import metrics as m
import pandas as pd
df_trades = pd.read_parquet('trades.parquet')

print('='* 40)
print(f'Win rate: {(m.calculate_win_rate('trades.parquet')):.2f}%')
print(f'Profit: {(m.calculate_final_profit('trades.parquet')):.2f} pts')
print(f'Number of trades: {m.calculate_trades_number('trades.parquet')}')
print(f'Profit per Trade: {m.calculate_profit_operations('trades.parquet')} pts')
print(f'Win Trades: {m.calculate_win_trades_number('trades.parquet')}')
print(f'Loss Trades: {m.calculate_loss_trades_number('trades.parquet')}')
print(f'Breakeven Trades: {m.calculate_breakeven('trades.parquet')}')
print(f'Profit per time ( 30min):\n {m.calculate_profit_by_time('trades.parquet')} ')
print(f'Acumulated Profit: {m.calculate_acumulated_profit('trades.parquet')} pts')
print(f'Highest Profit: {m.calculate_highest_profit('trades.parquet')} pts')
print(f'Max Drawdown: {m.calculate_drawdown('trades.parquet')} pts')
print('='* 40)
