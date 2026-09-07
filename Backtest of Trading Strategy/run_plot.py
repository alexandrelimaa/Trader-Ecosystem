import plot
import pandas as pd


df = pd.read_parquet("trades.parquet(1)")
print(plot.streak_loss_bar(df))