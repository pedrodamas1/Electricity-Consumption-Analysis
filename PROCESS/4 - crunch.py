'''
This script summarizes the monthly data by date
'''

import pandas as pd 
import numpy as np 
import re 

state = 'ASSIGNED'
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

# Generate a full data file
pd.concat( (pd.read_excel(path) for path in files), ignore_index=True ).to_excel('DATA/ASSIGNED/Consumos MINUTO.xlsx', index=False)

for path in files:
	# Start the analysis
	print(f"Starting the analysis of the file {path}")

	# Get the file info
	folder, state, year, month, extension = re.split('[/ .]', path)
	year = int(year)
	month = int(month)

	# Get the number of days in this month and load the data
	N_days = pd.Timestamp(year, month, 1).daysinmonth
	df = pd.read_excel(path)
	print(f"This month has {N_days} days and the loaded file has {len(df)} rows.")

	df = pd.melt(df, id_vars=['DATE', 'kWh', 'DT'], var_name='CYCLE', value_vars=['WEEKLY', 'DAILY'], value_name='PERIOD')
	pvt = pd.pivot_table(df, values=['DT', 'kWh'], index=['DATE', 'CYCLE', 'PERIOD'], aggfunc=np.sum).reset_index()

	path = 'DATA/CRUNCHED/{}/{:02}.xlsx'.format(year, month)
	pvt.to_excel(path, index=False)
	print("Sucessfully saved {} with a crunch factor of {:.2%} ".format(path, pvt.size/df.size))
	print("")

