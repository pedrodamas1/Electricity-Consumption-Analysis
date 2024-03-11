'''
This scripts summarizes the consumer data according to invoicing day of the month
'''

import pandas as pd 
import numpy as np 
import re 

# List the folders for analysis
paths = ['DATA/CRUNCHED/2022/{:02d}.xlsx'.format(month) for month in range(7,13)] + \
    ['DATA/CRUNCHED/2023/{:02d}.xlsx'.format(month) for month in range(1,13)]

# Merge all excel sheets and save daily consumption
df = pd.concat( (pd.read_excel(path) for path in paths), ignore_index=True )
df.to_excel('DATA/CRUNCHED/Consumos DAILY.xlsx', index=False)

# Shift according to GoldEnergy invoice date and save data
df['DATE'] = df['DATE'] - pd.DateOffset(days=21) + pd.DateOffset(months=1)
df['YEAR'] = df['DATE'].dt.year
df['MONTH'] = df['DATE'].dt.month

pvt = pd.pivot_table(df, values=['DT', 'kWh'], index=['YEAR', 'MONTH', 'CYCLE', 'PERIOD'], aggfunc='sum').reset_index()
path = 'DATA/CRUNCHED/Consumos OFFSET.xlsx'
pvt.to_excel(path, index=False)
print("Sucessfully saved {} with a crunch factor of {:.2%} ".format(path, pvt.size/df.size))

