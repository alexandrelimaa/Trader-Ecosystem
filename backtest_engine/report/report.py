from fpdf import FPDF
import pandas as pd
from metrics import formatting as fm
from metrics import period_metrics as pm
from metrics import profit_metrics as prm
from metrics import risk_metrics as rm
from metrics import time_metrics as tm

#Making the document
df = pd.read_parquet("../outputs/trades.parquet(1)")
pdf = FPDF()
pdf.add_page()

#Top
pdf.set_font('Times',style = 'B', size=20)
pdf.cell(90, 8, text='Backtest Report', new_x='LMARGIN', new_y='NEXT')
pdf.set_font('Times', size=12)

pdf.cell( 90, 8, text = f"Asset: WINFUT", new_x='LMARGIN', new_y='NEXT')
pdf.cell( 50, 8, text = f"Initial Date: {df['entry_time'].dt.date.min()}", new_x='RIGHT', new_y='TOP')
pdf.cell( 90, 8, text = f"Final Date: {df['entry_time'].dt.date.max()}", new_x='LMARGIN', new_y='NEXT')
pdf.cell( 90, 8, text = f"Number of Trades: {len(df)}", new_x='LMARGIN', new_y='NEXT')

#Adding all the text and the data from outputs
pdf.image('grafics/Equity Curve.png', x = 10, w = 200)
pdf.ln(5)
pdf.set_font('Times', size=16)
pdf.cell(0,10, text= "Profit metrics:", new_x='LMARGIN', new_y='NEXT')
pdf.ln(2.5)
pdf.set_font('Times', size=12)
pdf.cell(70,10, text = f"Final Profit points: {fm.format_points(prm.final_profit(df))}", new_x='RIGHT', new_y='TOP')
pdf.cell(55,10, text = f"Final Profit R$: {fm.convert_to_currency(prm.final_profit(df), 0.2)}", new_x='LMARGIN', new_y='NEXT')
pdf.cell(0,10, text = f"Profit per Trade: {fm.format_points(prm.profit_per_operations(df))}", new_x='LMARGIN', new_y='NEXT')
pdf.cell(0,10, text = f"Highest Profit: {fm.format_points(rm.highest_profit(df))}", new_x='LMARGIN', new_y='NEXT')
pdf.cell(70,10, text = f"Max Drawdown: {fm.format_points(rm.drawdown(df)['drawdown'].max())}", new_x='RIGHT', new_y='TOP')
pdf.cell(0,10, text = f"Max Drawdown: {fm.convert_to_currency(rm.drawdown(df)['drawdown'].max(), 0.2)}", new_x='LMARGIN', new_y='NEXT')
pdf.image('grafics/Drawdown_Curve.png', x = 10, w = 150)
pdf.ln(2.5)
pdf.cell(0,10, text = f"Win Rate: { fm.format_pct(prm.win_rate(df))}", new_x='LMARGIN', new_y='NEXT')
pdf.cell(55,10, text = f"Win Trades Number: {prm.win_trades_number(df)}", new_x='RIGHT', new_y='TOP')
pdf.cell(50,10, text = f"Loss Trades Number: {prm.loss_trades_number(df)}", new_x='LMARGIN', new_y='NEXT')
pdf.cell(0,10, text = f"Breakeven Trades Number: {prm.breakeven(df)}", new_x='LMARGIN', new_y='NEXT')
pdf.cell(0,10, text = f"Streak Loss: {rm.streak_losses(df)}", new_x='LMARGIN', new_y='NEXT')
pdf.image('grafics/Profit per trade Histogram.png', x = 10, w = 150)
pdf.ln(5)
pdf.cell(90,10, text = f"Profit Factor: {fm.format_round(prm.profit_factor(df))}", align = 'C', new_x='RIGHT', new_y='TOP')
pdf.cell(0,10, text = f"Expectancy: {fm.format_round(prm.expectancy_factor(df))}", new_x='LMARGIN', new_y='NEXT')
pdf.cell(90,10, text = f"Sharpe: {fm.format_round(rm.sharpe_ratio(df))}", align ='C', new_x='RIGHT', new_y='TOP')
pdf.cell(0,10, text = f"Sortino: {fm.format_round(rm.sortino_ratio(df))}", new_x='LMARGIN', new_y='NEXT')
pdf.ln(10)
pdf.set_font('Times', size=16)
pdf.cell(0, 10, text=f"Average Profit per :", new_x='LMARGIN', new_y='NEXT')
pdf.set_font('Times', size=12)
pdf.ln(2.5)
pdf.cell(50, 10, text=f"Day: {fm.format_points(pm.average_daily_profit(df))}", new_x='RIGHT', new_y='TOP')
pdf.cell(50, 10, text=f"Week: {fm.format_points(pm.average_weekly_profit(df))}", new_x='RIGHT', new_y='TOP')
pdf.cell(0, 10, text=f"Month: {fm.format_points(pm.average_monthly_profit(df))}", new_x='LMARGIN', new_y='NEXT')
pdf.image('grafics/Profit per days of the Week.png', x = 10, w = 200)
pdf.image('grafics/Profit_time_bars.png', x = 10, w = 200)
pdf.ln(2.5)
pdf.set_font('Times', size=16)
pdf.cell(0,10, text = 'Time:', new_x='LMARGIN', new_y='NEXT' )
pdf.set_font('Times', size=12)
pdf.ln(2.5)
pdf.cell(0,10, text = f"Average Time: {fm.format_min(tm.average_time(df))}", new_x='LMARGIN', new_y='NEXT')
pdf.cell(90,10, text = f"Maximum Time: {fm.format_min(tm.maximum_time(df))}", new_x='RIGHT', new_y='TOP')
pdf.cell(0,10, text = f"Minimum Time: {fm.format_min(tm.minimum_time(df))}", new_x='LMARGIN', new_y='NEXT')

pdf.output('../report/results/report.pdf')