from report.metrics import risk_metrics as rm
from report.metrics import period_metrics as pm
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
    plt.savefig('Equity Curve.png', dpi=300)
    plt.show()
    plt.close()

def drawdown_curve(df):
    """ Grafic, Drawdown curve for trading strategies"""
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
    plt.savefig('Drawdown_curve.png', dpi=150)
    plt.show()
    plt.close()

def profit_time_bars(df):
    """Grafic Profit times bars for trading strategies"""
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
    plt.savefig('Profit_time_bars.png', dpi=150)
    plt.show()
    plt.close()


def profit_distribution(df):
    """ GraficsProfit by trade"""
    plt.figure(figsize= ( 25, 7 ))
    plt.hist(df['profit'], bins = 30)
    plt.title('Profit Distribution')
    plt.xlabel('Profit per Trade')
    plt.ylabel('Frequency')
    plt.grid(True, alpha=0.3)
    plt.axvline(x=0, color='gray', linestyle='--', linewidth=0.8)
    plt.savefig('Profit per trade Histogram.png', dpi=150)
    plt.show()
    plt.close()


def profit_weekday_bars(df):
    """ grafics Profit weekday bars for trading strategies"""
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
    plt.savefig('Profit per days of the Week.png', dpi=150)
    plt.show()
    plt.close()

def streak_loss_bar(df):
    """ grafics Streak loss bars for trading strategies"""
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
    plt.savefig('Streak Loss.png', dpi=150)
    plt.show()
    plt.close()

def daily_trades_grafic(df):
    """grafics of Average daily trades  for trading strategies"""
    data = pm.daily_profit(df)
    x_line = data['data_bucket'].astype('str')
    y_line = data['daily_profit'].astype('float')
    y_line = data['profit']
    plt.figure(figsize= ( 25, 7 ))
    plt.bar(x_line, y_line, color = np.where(y_line > 0, 'green', 'red'))
    plt.title('Profit per date')
    plt.xlabel('Day')
    plt.ylabel('Number of Trades')
    plt.grid(True, alpha=0.3)
    plt.axhline(y=0, color='gray', linestyle='--', linewidth=0.8)
    plt.savefig('Profit per date.png', dpi=150)
    plt.show()
    plt.close()


def weekly_trades_grafic(df):
    """grafics of Average weekly trades  for trading strategies"""
    data = pm.weekly_profit(df)
    x_line = data['week_bucket'].astype('str')
    y_line = data['profit']
    plt.figure(figsize= ( 25, 7 ))
    plt.bar(x_line, y_line, color = np.where(y_line > 0, 'green', 'red'))
    plt.title('Profit per week')
    plt.xlabel('Week')
    plt.ylabel('Profit')
    plt.grid(True, alpha=0.3)
    plt.axhline(y=0, color='gray', linestyle='--', linewidth=0.8)
    plt.savefig('Profit per Week.png', dpi=150)
    plt.show()
    plt.close()

def montly_trades_grafic(df):
    """grafics of Average monthly trades  for trading strategies"""
    data = pm.monthly_profit(df)
    x_line = data['month_bucket'].astype('str')
    y_line = data['profit']
    plt.figure(figsize= ( 25, 7 ))
    plt.bar(x_line, y_line, color = np.where(y_line > 0, 'green', 'red'))
    plt.title('Profit per Month')
    plt.xlabel('Month')
    plt.ylabel('Profit')
    plt.grid(True, alpha=0.3)
    plt.axhline(y=0, color='gray', linestyle='--', linewidth=0.8)
    plt.savefig('Profit per Month.png', dpi=150)
    plt.show()
    plt.close()

def number_trades_daily_grafic(df):
    """grafics of Average number of daily trades  for trading strategies"""
    data = pm.average_number_daily_trades(df)
    x_line = data['data_bucket'].astype('str')
    y_line = data['number'].astype('float')
    plt.figure(figsize= ( 25, 7 ))
    plt.bar(x_line, y_line)
    plt.title('Number of Daily Trades')
    plt.xlabel('Date')
    plt.ylabel('Number Trades')
    plt.grid(True, alpha=0.3)
    plt.savefig('Number of Daily Trades.png', dpi=150)
    plt.show()
    plt.close()

def number_trades_weekly_grafic(df):
    """grafics of Average number of weekly trades  for trading strategies"""
    data = pm.average_number_week_trades(df)
    x_line = data['week_bucket'].astype('str')
    y_line = data['number'].astype('float')
    plt.figure(figsize= ( 25, 7 ))
    plt.bar(x_line, y_line)
    plt.title('Number of Week Trades')
    plt.xlabel('Week')
    plt.ylabel('Number Trades')
    plt.grid(True, alpha=0.3)
    plt.savefig('Number of Week Trades.png', dpi=150)
    plt.show()
    plt.close()

def number_trades_monthly_grafic(df):
    """grafics of Average number of monthly trades  for trading strategies"""
    data = pm.average_number_month_trades(df)
    x_line = data['month_bucket'].astype('str')
    y_line = data['number'].astype('float')
    plt.figure(figsize= ( 25, 7 ))
    plt.bar(x_line, y_line)
    plt.title('Number of Monthly Trades')
    plt.xlabel('Date')
    plt.ylabel('Number Trades')
    plt.grid(True, alpha=0.3)
    plt.savefig('Number of Monthly Trades.png', dpi=150)
    plt.show()
    plt.close()
