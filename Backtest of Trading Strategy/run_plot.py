import plot
import pandas as pd


df = pd.read_parquet("trades.parquet(1)")
plot.profit_time_bars(df)