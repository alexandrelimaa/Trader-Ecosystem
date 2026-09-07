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
pdf.set_font('Helvetica', size=12)
pdf.cell(0, 10, text='Backtest Report', new_x='LMARGIN', new_y='NEXT')
pdf.cell(0,10, text =f"Win Rate:{ fm.format_pct(prm.win_rate(df))}", new_x='LMARGIN', new_y='NEXT')
pdf.cell( 0, 10, text = f"")







pdf.cell( 0, 10, text = f"")
#pdf.image('Grafics/Equity Curve.png', x = 10, w = 277)
pdf.output('teste.pdf')

