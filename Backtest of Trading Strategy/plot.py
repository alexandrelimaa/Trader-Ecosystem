from Metrics import risk_metrics as rm
from Metrics import period_metrics as pm
import matplotlib.pyplot as plt


def equity_curve(df):
    """Equity curve for trading strategies"""
    data = rm.accumulated_profit(df)
    x_line = data['entry_time']
    y_line = data['accumulated_profit']
    plt.figure(figsize= ( 25, 7 ))
    plt.plot(x_line, y_line)
    plt.title('Equity Curve')
    plt.xlabel('Time')
    plt.ylabel('Accumulated Profit')
    plt.grid(True, alpha=0.3)
    plt.axhline(y=0, color='gray', linestyle='--', linewidth=0.8)
    plt.savefig('Grafics/Equity_curve.png', dpi=150)
    plt.show()
    plt.close()

def drawdown_curve(df):
    """Drawdown curve for trading strategies"""
    data = rm.drawdown(df)
    x_line = data['entry_time']
    y_line = data['drawdown']
    plt.figure(figsize= ( 25, 7 ))
    plt.plot(x_line, y_line)
    plt.title('Drawdown Curve')
    plt.xlabel('Time')
    plt.ylabel('Drawdown')
    plt.grid(True, alpha=0.3)
    plt.axhline(y=0, color='gray', linestyle='--', linewidth=0.8)
    plt.savefig('Grafics/Drawdown_curve.png', dpi=150)
    plt.show()
    plt.close()

def profit_time_bars(df):
    """Profit times bars for trading strategies"""
    data = pm.profit_by_time(df)
    x_bar = data['time_bucket'].astype('str')
    y_bar = data['profit']
    plt.figure(figsize= ( 25, 7 ))
    plt.barh(x_bar, y_bar)
    plt.title('Profit Time Bars')
    plt.xlabel('Time')
    plt.ylabel('Profit')
    plt.grid(True, alpha=0.3)
    plt.axvline(x=0, color='gray', linestyle='--', linewidth=0.8)
    plt.savefig('Grafics/Profit_time_bars.png', dpi=150)
    plt.show()
    plt.close()



