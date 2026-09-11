from report.grafics import plot
import pandas as pd

df = pd.read_parquet("../outputs/trades.parquet(1)")
plot.equity_curve(df)
plot.drawdown_curve(df)
plot.profit_time_bars(df)
plot.profit_distribution(df)
plot.profit_weekday_bars(df)
plot.streak_loss_bar(df)
plot.daily_trades_grafic(df)
plot.weekly_trades_grafic(df)
plot.montly_trades_grafic(df)
plot.number_trades_daily_grafic(df)
plot.number_trades_weekly_grafic(df)
plot.number_trades_monthly_grafic(df)
