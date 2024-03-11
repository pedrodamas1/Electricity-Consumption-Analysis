'''
YEAR	MONTH	WEEKDAY	HOUR	PERIOD	DT	KWH

'''

import os 
import pandas as pd 
import numpy as np 

# Define the data time interval in minutes
dt = 15.

# Merge all excel sheets
raw = pd.concat( [pd.read_excel('DATA/CORRECTED/'+file) for file in os.listdir('DATA/CORRECTED')], ignore_index=True )

# Generate a new dataframe
df = pd.DataFrame()
df['DATETIME'] = pd.to_datetime(raw['Data'] + ' ' + raw['Hora'])
df['kWh'] = raw['kW'] * dt/60.
df['DT'] = dt/60./24.
df.sort_values(by='DATETIME', inplace=True)

# Remove duplicates
print(f"There are no duplicates by TIMESTAMP: { df[df.duplicated('DATETIME')].empty }")
print(f"There are no duplicates by ROW: { df[df.duplicated()].empty }")

# Now, let's validate the cleaning done
validation = df.copy()
validation['YEAR'] = validation['DATETIME'].dt.year
validation['MONTH'] = validation['DATETIME'].dt.month
validation['DATETIME'].apply( lambda x: x.month )
validation = validation.pivot_table(values=['DATETIME'], index=['YEAR', 'MONTH'], aggfunc=len).reset_index()
validation['COUNT'] = validation[['YEAR', 'MONTH']].apply(lambda x: pd.Timestamp(x.YEAR, x.MONTH, 1).daysinmonth*24*4, axis=1)
validation['CHECK'] = validation[['DATETIME', 'COUNT']].apply(lambda x: "" if x.DATETIME==x.COUNT else 'x', axis=1)
print(f"The count of datetime entries must match the expected number of rows per month:")
print(validation)
print('')

# Also check the continuity of time
prev = df.loc[0, 'DATETIME'] - pd.Timedelta(minutes=dt)
for _, row in df.iterrows():
	curr = row.DATETIME
	delta = curr - prev
	prev = curr
	if delta != pd.Timedelta(minutes=dt):
		print(curr)


# Load the tariffs data
tariffs = pd.read_excel('INFO/TARIFAS.xlsx', sheet_name='TARIFAS')

# Return the weekly and daily tariff for some timestamp
count = 1
def get_tariff(timestamp:pd.Timestamp):
	global count
	print("\rProgress:  {:6}/{} \t {} ".format(count, N, timestamp) , end='')
	count += 1

	def get_season(timestamp:pd.Timestamp):
		if 5 < timestamp.month < 11:
			return 'SUMMER'
		else:
			return 'WINTER'

	# Get necessary datetime properties
	date = timestamp.date()
	time = timestamp.time()
	weekday = timestamp.day_name()
	season = get_season(timestamp)
	
	# Make a filter
	selec = tariffs[
		(tariffs.SEASON.str.contains(season, case=False)) & 
		(tariffs.WEEKDAY.str.contains(weekday, case=False)) & 
		(tariffs.START <= time) & 
		(time <= tariffs.END)
	].set_index('CYCLE')

	# Validate size of result
	if len(selec) != 2:
		raise ValueError(f"Tariff calculation failed for the timestamp: {timestamp} ")

	# Return pandas series
	return pd.Series([selec.loc['WEEKLY', 'PERIOD'], selec.loc['DAILY', 'PERIOD']])


# Determine the tariffs
N = len(df)
print(f"Number of tariffs to calculate: {N} ")
df[['WEEKLY', 'DAILY']] = df['DATETIME'].apply(get_tariff)
print('')

# Create two separate sheets, pivoting by date
df['DATE'] = df['DATETIME'].dt.date

# Generate separate results for weekly and daily cycles
df_weekly = df.copy()
df_weekly.drop(['DATETIME', 'DAILY'], axis=1, inplace=True)
df_weekly.rename(columns={"WEEKLY": "PERIOD"}, inplace=True)

df_daily = df.copy()
df_daily.drop(['DATETIME', 'WEEKLY'], axis=1, inplace=True)
df_daily.rename(columns={"DAILY": "PERIOD"}, inplace=True)

# Save to excel as pivot tables
with pd.ExcelWriter("DATA/consumos.xlsx") as writer:
	pd.pivot_table(df_weekly, values=['DT', 'kWh'], index=['DATE', 'PERIOD'], aggfunc=np.sum).reset_index().to_excel(writer, sheet_name="WEEKLY", index=False)
	pd.pivot_table(df_daily, values=['DT', 'kWh'], index=['DATE', 'PERIOD'], aggfunc=np.sum).reset_index().to_excel(writer, sheet_name="DAILY", index=False)




