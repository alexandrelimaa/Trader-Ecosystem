from fpdf import FPDF
import pandas as pd
from Metrics import formatting as fm
from Metrics import period_metrics as pm
from Metrics import profit_metrics as prm
from Metrics import risk_metrics as rm
from Metrics import time_metrics as tm


df = pd.read_parquet("trades.parquet(1)")
pdf = FPDF()
pdf.add_page()
pdf.set_font('Times', size=12)

#Cabeçario
pdf.set_font('Times',style = 'B', size=20)
pdf.cell(0, 10, text='Backtest Report', new_x='LMARGIN', new_y='NEXT')
pdf.set_font('Times', size=12)
#Ideia da estrategia ou nome nao sei
pdf.cell( 0, 10, text = f"Asset: WINFUT", new_x='LMARGIN', new_y='NEXT') # Change here so its automatic later
pdf.cell( 0, 10, text = f"Initial Date: {df['entry_time'].dt.date.min()}", new_x='LMARGIN', new_y='NEXT')
pdf.cell( 0, 10, text = f"Final Date: {df['entry_time'].dt.date.max()}", new_x='LMARGIN', new_y='NEXT')
pdf.cell( 0, 10, text = f"Number of Trades: {len(df)}", new_x='LMARGIN', new_y='NEXT')
pdf.ln(10)

#Profit Metrics
pdf.set_font('Times', size=16)
pdf.cell(0,10, text= "Profit Metrics:", new_x='LMARGIN', new_y='NEXT')
pdf.ln(2.5)
pdf.set_font('Times', size=12)
pdf.cell(0,10, text = f"Win Rate: { fm.format_pct(prm.win_rate(df))}", new_x='LMARGIN', new_y='NEXT')
pdf.cell(0,10, text = f"Final Profit: {fm.format_points(prm.final_profit(df))}", new_x='LMARGIN', new_y='NEXT')
pdf.cell(0,10, text = f"Profit per Trade: {fm.format_points(prm.profit_per_operations(df))}", new_x='LMARGIN', new_y='NEXT')
pdf.cell(0,10, text = f"Win Trades Number: {prm.win_trades_number(df)}", new_x='LMARGIN', new_y='NEXT')
pdf.cell(0,10, text = f"Loss Trades Number: {prm.loss_trades_number(df)}", new_x='LMARGIN', new_y='NEXT')
pdf.cell(0,10, text = f"Breakeven Trades Number: {prm.breakeven(df)}", new_x='LMARGIN', new_y='NEXT')
pdf.cell(0,10, text = f"Profit Factor: {fm.format_round(prm.profit_factor(df))}", new_x='LMARGIN', new_y='NEXT')
pdf.cell(0,10, text = f"Expectancy: {fm.format_round(prm.expectancy_factor(df))}", new_x='LMARGIN', new_y='NEXT')
pdf.ln(10)

#Risk Metrics
pdf.set_font('Times', size=16)
pdf.cell(0,10, text = "Risk Metrics:", new_x='LMARGIN', new_y='NEXT')
pdf.ln(2.5)
pdf.set_font('Times', size=12)
pdf.cell(0,10, text = f"Highest Profit: {fm.format_points(rm.highest_profit(df))}", new_x='LMARGIN', new_y='NEXT')
pdf.cell(0,10, text = f"Max Drawdown: {fm.format_points(rm.drawdown(df)['drawdown'].max())}", new_x='LMARGIN', new_y='NEXT')
pdf.cell(0,10, text = f"Streak Loss: {rm.streak_losses(df)}", new_x='LMARGIN', new_y='NEXT')
pdf.cell(0,10, text = f"Sharpe: {fm.format_round(rm.sharpe_ratio(df))}", new_x='LMARGIN', new_y='NEXT')
pdf.cell(0,10, text = f"Sortino: {fm.format_round(rm.sortino_ratio(df))}", new_x='LMARGIN', new_y='NEXT')
pdf.ln(10)

#Period Metrics
pdf.set_font('Times', size=16)
pdf.cell(0,10, text = f"Period Metrics:", new_x='LMARGIN', new_y='NEXT')
pdf.ln(2.5)
pdf.set_font('Times', size=12)
pdf.cell(0,10, text = f"Daily Profit: {pm.daily_profit(df)}", new_x='LMARGIN', new_y='NEXT')
pdf.cell(0,10, text = f"Weekly Profit: {pm.weekly_profit(df)}", new_x='LMARGIN', new_y='NEXT')
pdf.cell(0,10, text = f"Monthly Profit: {pm.monthly_profit(df)}", new_x='LMARGIN', new_y='NEXT')
pdf.cell(0,10, text = f"Average Number of Trade per :", new_x='LMARGIN', new_y='NEXT')
pdf.cell(0,10, text = f"Day: {pm.average_number_daily_trades(df)}", new_x='LMARGIN', new_y='NEXT')
pdf.cell(0,10, text = f"Week: {pm.average_number_week_trades(df)}", new_x='LMARGIN', new_y='NEXT')
pdf.cell(0,10, text = f"Month: {pm.average_number_month_trades(df)}", new_x='LMARGIN', new_y='NEXT')
pdf.cell(0, 10, text=f"Average Profit per :", new_x='LMARGIN', new_y='NEXT')
pdf.cell(0, 10, text=f"Day: {fm.format_points(pm.average_daily_profit(df))}", new_x='LMARGIN', new_y='NEXT')
pdf.cell(0, 10, text=f"Week: {fm.format_points(pm.average_weekly_profit(df))}", new_x='LMARGIN', new_y='NEXT')
pdf.cell(0, 10, text=f"Month: {fm.format_points(pm.average_monthly_profit(df))}", new_x='LMARGIN', new_y='NEXT')
pdf.ln(10)

#Time Metrics
pdf.set_font('Times', size=16)
pdf.cell(0,10, text = "Time Metrics:", new_x='LMARGIN', new_y='NEXT')
pdf.ln(2.5)
pdf.set_font('Times', size=12)
pdf.cell(0,10, text = f"Average Time: {fm.format_min(tm.average_time(df))}", new_x='LMARGIN', new_y='NEXT')
pdf.cell(0,10, text = f"Maximum Time: {fm.format_min(tm.maximum_time(df))}", new_x='LMARGIN', new_y='NEXT')
pdf.cell(0,10, text = f"Minimum Time: {fm.format_min(tm.minimum_time(df))}", new_x='LMARGIN', new_y='NEXT')

#pdf.cell(0,10, text = f"")
#pdf.set_font('Times', size=12)
#pdf.ln(10)
#pdf.image('Grafics/Equity Curve.png', x = 10, w = 277)
pdf.output('teste.pdf')

