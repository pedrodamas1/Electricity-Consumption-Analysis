'''
This script assigns a tariff to each 15 minute interval and summarizes the data on a daily basis
'''

import pandas as pd 
import re 

paths = ['DATA/CORRECTED/2022/{:02d}.xlsx'.format(month) for month in range(7,13)] + \
    ['DATA/CORRECTED/2023/{:02d}.xlsx'.format(month) for month in range(1,13)]

# Load the tariffs data
tariffs = pd.read_excel('INFO/TARIFAS.xlsx', sheet_name='TARIFAS')

# Return the weekly and daily tariff for some timestamp
def get_tariff(row):
	global count
	print("\rProgress:  {:6}/{} \t {} ".format(count, N, row.DATETIME) , end='')
	count += 1
	
	# Make a filter
	selec = tariffs[
		(tariffs.SEASON.str.contains(row.SEASON, case=False)) & 
		(tariffs.WEEKDAY.str.contains(row.WEEKDAY, case=False)) & 
		(tariffs.START <= row.TIME) & 
		(row.TIME <= tariffs.END)
	].set_index('CYCLE')

	# Validate size of result
	if len(selec) != 2:
		raise ValueError(f"Tariff calculation failed for the timestamp: {row.DATETIME} ")

	# Return pandas series
	return pd.Series([selec.loc['WEEKLY', 'PERIOD'], selec.loc['DAILY', 'PERIOD']])


for path in paths:
	# Start the analysis
	print(f"Starting the analysis of the file {path}")
	# Get the file info
	folder, state, year, month, extension = re.split('[/ .]', path)
	year = int(year)
	month = int(month)

	# Get the number of days in this month and load the data
	N_days = pd.Timestamp(year, month, 1).daysinmonth
	df = pd.read_excel(path, skiprows=7)
	print(f"This month has {N_days} days and the loaded file has {len(df)} rows.")

	# Generate useful columns
	df['DATETIME'] = pd.to_datetime(df['Data'] + ' ' + df['Hora'])
	df.rename(columns={"Consumo registado, Ativa": "kW"}, inplace=True)
	df.sort_values(by='DATETIME', inplace=True)
	df['YEAR'] = df['DATETIME'].dt.year
	df['MONTH'] = df['DATETIME'].dt.month
	df['DATE'] = df['DATETIME'].dt.date
	df['TIME'] = df['DATETIME'].dt.time
	df['WEEKDAY'] = df['DATETIME'].dt.day_name()
	df['SEASON'] = df['MONTH'].apply(lambda month: 'SUMMER' if 5 < month < 11 else 'WINTER')
	df['kWh'] = df['kW'] * 15/60.
	df['DT'] = 15/60./24.

	# Determine the tariffs
	N = len(df)
	count = 1
	print(f"Number of tariffs to calculate: {N} ")
	df[['WEEKLY', 'DAILY']] = df.apply(get_tariff, axis=1)
	print('')

	path = 'DATA/ASSIGNED/{}/{:02}.xlsx'.format(year, month)
	df.to_excel(path, index=False)
	print(f"Sucessfully saved {path}")
	print("")

