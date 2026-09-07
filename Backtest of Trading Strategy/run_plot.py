import plot
import pandas as pd


df = pd.read_parquet("trades.parquet(1)")
print(plot.equity_curve(df))