#!/usr/bin/python3

#first install the packages below:
#pip install sklearn
#pip install quandl
#pip install pandas

import pandas as pd
import quandl

df = quandl.get('WIKI/GOOGL')

print(df.head)
