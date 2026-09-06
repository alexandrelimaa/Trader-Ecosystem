import os
import glob
candle_files_pattern = "Files/Minutes of WINFUT/candle_*.csv"
tick_files_pattern = "Files/Ticks of WINFUT/tick_*.csv"

files = glob.glob(tick_files_pattern)
for f in files:
    size_mb = os.path.getsize(f) / (1024 * 1024)
    print(f"{f}: {size_mb:.1f} MB")