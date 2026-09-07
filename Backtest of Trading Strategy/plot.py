from Metrics import risk_metrics as rm
from Metrics import period_metrics as pm
import matplotlib.pyplot as plt
import numpy as np


def equity_curve(df):
    """Equity curve for trading strategies"""
    data = rm.accumulated_profit(df)
    x_line = data['entry_time']
    y_line = data['accumulated_profit']
    plt.figure(figsize= ( 30, 8 ))
    plt.plot(x_line, y_line)
    plt.title('Equity Curve')
    plt.xlabel('Time')
    plt.ylabel('Accumulated Profit')
    plt.grid(True, alpha=0.3)
    plt.axhline(y=0, color='gray', linestyle='--', linewidth=0.8)
    plt.savefig('Grafics/Equity Curve.png', dpi=300)
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


def profit_distribution(df):
    """Profit by trade"""
    plt.figure(figsize= ( 25, 7 ))
    plt.hist(df['profit'], bins = 30)
    plt.title('Profit Distribution')
    plt.xlabel('Profit per Trade')
    plt.ylabel('Frequency')
    plt.grid(True, alpha=0.3)
    plt.axvline(x=0, color='gray', linestyle='--', linewidth=0.8)
    plt.savefig('Grafics/Profit per trade Histogram.png', dpi=150)
    plt.show()
    plt.close()


def profit_weekday_bars(df):
    """Profit weekday bars for trading strategies"""
    data = pm.profit_weekday(df)
    x_bar = data['profit']
    y_bar = data['weekday_bucket'].astype('str')
    plt.figure(figsize= ( 25, 7 ))
    plt.barh(y_bar, x_bar)
    plt.title('Profit per day of the Week')
    plt.xlabel('Profit')
    plt.ylabel('Day of the week')
    plt.grid(True, alpha=0.3)
    plt.axvline(x=0, color='gray', linestyle='--', linewidth=0.8)
    plt.savefig('Grafics/Profit per days of the Week.png', dpi=150)
    plt.show()
    plt.close()

def streak_loss_bar(df):
    """Streak loss bars for trading strategies"""
    df = df.copy()
    df = df.sort_values('entry_time').reset_index(drop=True)
    y_line = np.where(df['profit'] > 0, 1, -1)
    x_line = range(len(df))
    plt.figure(figsize= ( 25, 7 ))
    plt.bar(x_line, y_line, color = np.where(y_line > 0, 'green', 'red'))
    plt.title('Streak Loss Bars')
    plt.xlabel('trade number')
    plt.ylabel('Streak Loss')
    plt.grid(True, alpha=0.3)
    plt.axhline(y=0, color='gray', linestyle='--', linewidth=0.8)
    plt.show()
    plt.close()
