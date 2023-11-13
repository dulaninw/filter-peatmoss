import os
import pandas as pd

# There are a number of CSVs in the current directory.
# Merge them into a single CSV.
# The CSVs have the same columns.
for file in os.listdir('.'):
    if file.endswith('.csv'):
        df = pd.read_csv(file)
        df.to_csv('merged.csv', mode='a', index=False, header=False)

