#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import pandas as pd
import quandl
import math

df = quandl.get('WIKI/GOOGL')

df = df[['Adj. Open', 'Adj. High', 'Adj. Low', 'Adj. Close', 'Adj. Volume',]]

df['HL_PERCENT'] = (df['Adj. High'] - df['Adj. Close']) / df['Adj. Close'] * 100.0
df['HL_CHANGE'] = (df['Adj. Close'] - df['Adj. Open']) / df['Adj. Open'] * 100.0

df = df[['Adj. Close', 'HL_PERCENT', 'HL_CHANGE', 'Adj. Volume']]

#print(df.head())

forecast_col = 'Adj.Close'
df.fillna(-99999, inplace = True)

forecast_out = int(math.ceil(0.1 * len(df)))

df['label'] = df[forecast_col].shift(-forecast_out)

print(df.head())