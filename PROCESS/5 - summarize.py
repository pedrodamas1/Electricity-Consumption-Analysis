'''
This scripts summarizes the consumer data according to GOLDENERGY calendar: 22nd of month N to 21st of month N+1
'''

import pandas as pd 
import numpy as np 
import re 

state = 'CRUNCHED'
# List the folders for analysis
files = [
    f'DATA/{state}/2022/07.xlsx',
    f'DATA/{state}/2022/08.xlsx',
    f'DATA/{state}/2022/09.xlsx',
    f'DATA/{state}/2022/10.xlsx',
    f'DATA/{state}/2022/11.xlsx',
    f'DATA/{state}/2022/12.xlsx',
    f'DATA/{state}/2023/01.xlsx',
    f'DATA/{state}/2023/02.xlsx',
    f'DATA/{state}/2023/03.xlsx',
    f'DATA/{state}/2023/04.xlsx',
    f'DATA/{state}/2023/05.xlsx',
    f'DATA/{state}/2023/06.xlsx',
    f'DATA/{state}/2023/07.xlsx',
    f'DATA/{state}/2023/08.xlsx',
    f'DATA/{state}/2023/09.xlsx',
    f'DATA/{state}/2023/10.xlsx',
    f'DATA/{state}/2023/11.xlsx',
    f'DATA/{state}/2023/12.xlsx',
]


# Merge all excel sheets and save daily consumption
df = pd.concat( (pd.read_excel(path) for path in files), ignore_index=True )
df.to_excel('DATA/CRUNCHED/Consumos DIA.xlsx', index=False)

# Shift according to GoldEnergy invoice date and save data
df['DATE'] = df['DATE'] - pd.DateOffset(days=21) + pd.DateOffset(months=1)
df['YEAR'] = df['DATE'].dt.year
df['MONTH'] = df['DATE'].dt.month

pvt = pd.pivot_table(df, values=['DT', 'kWh'], index=['YEAR', 'MONTH', 'CYCLE', 'PERIOD'], aggfunc=np.sum).reset_index()
path = 'DATA/CRUNCHED/Consumos GOLDENERGY.xlsx'
pvt.to_excel(path, index=False)
print("Sucessfully saved {} with a crunch factor of {:.2%} ".format(path, pvt.size/df.size))

