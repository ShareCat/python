#!/usr/bin/python3

import pandas as pd
import quandl

df = quandl.get('WIKI/GOOGL')

df = df[['Adj. Open', 'Adj. High', 'Adj. Low', 'Adj. Close', 'Adj. Volume',]]

df['HL_PERCENT'] = (df['Adj. High'] - df['Adj. Close']) / df['Adj. Close'] * 100.0

print(df.head())
