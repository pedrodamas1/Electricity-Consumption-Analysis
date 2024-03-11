'''
The aim of this script is to validate the exported monthly data, checking if:
- it starts at 00:00:00 of day 1
- it ends at 23:45:00 of the last day (variable)
- has the correct number of entries
- has 15 minute time intervals throughout
- all entries correspond to the correct month and year
- check for duplicate rows
'''

import pandas as pd 
import re 
from colorama import Fore, Style

# List the folders for analysis
state = 'RAW'
state = 'CORRECTED'
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

for path in files:
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

    # Generate a DATETIME column and sort it chronologically
    df['DATETIME'] = pd.to_datetime(df['Data'] + ' ' + df['Hora'])
    df.sort_values(by='DATETIME', inplace=True)
    df['YEAR'] = df['DATETIME'].dt.year
    df['MONTH'] = df['DATETIME'].dt.month

    # Check if the dataframe start with the correct datetime
    row = df.iloc[0].DATETIME
    start = pd.Timestamp(year=year, month=month, day=1)
    if row == start:
        print("[{}{:^10}{}] Initial timestamp validated.".format(Fore.GREEN, 'OK', Style.RESET_ALL))
    else:
        print("[{}{:^10}{}] Initial timestamp should be {} but {} was found.".format(Fore.RED, 'ERROR', Style.RESET_ALL, start, row))

    # Check if the dataframe end with the correct datetime
    row = df.iloc[-1].DATETIME
    end = pd.Timestamp(year=year, month=month, day=N_days, hour=23, minute=45)
    if row == end:
        print("[{}{:^10}{}] Final timestamp validated.".format(Fore.GREEN, 'OK', Style.RESET_ALL))
    else:
        print("[{}{:^10}{}] Final timestamp should be {} but {} was found.".format(Fore.RED, 'ERROR', Style.RESET_ALL, end, row))

    # Check there are entries only for the supposed year
    if set(df.MONTH) == {month}:
        print("[{}{:^10}{}] Month validated.".format(Fore.GREEN, 'OK', Style.RESET_ALL))
    else:
        print("[{}{:^10}{}] Expected to find only the month {} but found {}.".format(Fore.RED, 'ERROR', Style.RESET_ALL, month, set(df.MONTH)))

    # Check there are entries only for the supposed year
    if set(df.YEAR) == {year}:
        print("[{}{:^10}{}] Year validated.".format(Fore.GREEN, 'OK', Style.RESET_ALL))
    else:
        print("[{}{:^10}{}] Expected to find only the year {} but found {}.".format(Fore.RED, 'ERROR', Style.RESET_ALL, year, set(df.YEAR)))

    # Check if the file has the expected number of rows
    size = N_days*24*4
    if len(df) == size:
        print("[{}{:^10}{}] Dataframe size validated.".format(Fore.GREEN, 'OK', Style.RESET_ALL))
    else:
        print("[{}{:^10}{}] Expected to find {} rows of data, but found {}.".format(Fore.RED, 'ERROR', Style.RESET_ALL, size, len(df)))

    # Check for duplicate rows overall
    df_dup = df[df.duplicated()]
    if df_dup.empty:
        print("[{}{:^10}{}] Absence of duplicates validated.".format(Fore.GREEN, 'OK', Style.RESET_ALL))
    else:
        print("[{}{:^10}{}] duplicate rows were found overall.".format(Fore.RED, 'ERROR', Style.RESET_ALL))
        print(df_dup)

    # Check for specific duplicate rows
    df_dup = df[df.duplicated('DATETIME')]
    if df_dup.empty:
        print("[{}{:^10}{}] Absence of duplicates by DATETIME validated.".format(Fore.GREEN, 'OK', Style.RESET_ALL))
    else:
        print("[{}{:^10}{}] duplicate rows by DATETIME were found.".format(Fore.RED, 'ERROR', Style.RESET_ALL))
        print(df_dup)

    # Check that rows are equally time-spaced in 15-minute intervals
    prev = df.iloc[0].DATETIME - pd.DateOffset(minutes=15)
    success = True
    for i, row in df.iterrows():
        now = row.DATETIME
        delta = now - prev
        prev = now

        if delta != pd.Timedelta(minutes=15):
            print("[{}{:^10}{}] An error was found in time-spacing on the {}.".format(Fore.RED, 'ERROR', Style.RESET_ALL, now))
            success = False
    
    if success:
        print("[{}{:^10}{}] Time spacing validated.".format(Fore.GREEN, 'OK', Style.RESET_ALL))
    else:
        print("[{}{:^10}{}] Time spacing validation unsuccessful.".format(Fore.RED, 'ERROR', Style.RESET_ALL))
    
    print("")

    




# import os 
# import pandas as pd 
# import numpy as np 

# # Start by fetching all data in a single list of dataframes
# data_path = 'DATA/RAW'
# data = []
# for year in os.listdir(data_path):
#     for file in os.listdir("{}/{}".format(data_path, year)):
#         temp = pd.read_excel("{}/{}/{}".format(data_path, year, file), skiprows=7)
#         data.append(temp)

# # Join the data of all months
# raw = pd.concat(data, ignore_index=True)

# # Generate a new dataframe
# df = pd.DataFrame()
# df['DATETIME'] = pd.to_datetime(raw['Data'] + ' ' + raw['Hora'])
# df['kWh'] = raw['Consumo registado, Ativa'] * 15./60.
# df.sort_values(by='DATETIME', inplace=True)

# # Remove duplicates
# df1 = df[df.duplicated('DATETIME')]
# print(f"Start by viewing {len(df1)} duplicate values by TIMESTAMP:")
# print(df1)
# print('')

# df2 = df[df.duplicated()]
# print(f"Also view {len(df2)} ROW duplicates - undubious:")
# print(df2)
# print('')

# # Remove the obvious duplicates
# df.drop_duplicates(inplace=True)

# # View what is left
# df1 = df[df.duplicated('DATETIME')]
# print(f"There are still {len(df1)} duplicate values by TIMESTAMP:")
# print(df1)
# print('')

# # We have no clue what the right values are. Thus, the values were manually fixed in the CORRECTED folder according to the e-Redes website
# # Two main issues were found:
# # 	1 - the exported data for the first months starts at 1am on day 1 and ends at 1am on day one of the next month
# # 	2 - the month of October, on day 30, has the times of 1:00, 1:15, 1:30 and 1:45 repeated three times...
# df.drop_duplicates(subset=['DATETIME'], inplace=True)

# # Now, let's validate the cleaning done
# validation = df.copy()
# validation['YEAR'] = validation['DATETIME'].dt.year
# validation['MONTH'] = validation['DATETIME'].dt.month
# #validation['DATETIME'].apply( lambda x: x.month )
# validation = validation.pivot_table(values=['DATETIME'], index=['YEAR', 'MONTH'], aggfunc=len).reset_index()
# validation['COUNT'] = validation[['YEAR', 'MONTH']].apply(lambda x: pd.Timestamp(x.YEAR, x.MONTH, 1).daysinmonth*24*4, axis=1)
# validation['CHECK'] = validation[['DATETIME', 'COUNT']].apply(lambda x: "" if x.DATETIME==x.COUNT else 'x', axis=1)

# print(f"The count of datetime entries must match the expected number of rows per month:")
# print(validation)
# print('')

# # Drop the unnecessary columns
# df.drop(['YEAR', 'MONTH'], axis=1, inplace=True)
# df.reset_index(inplace=True)

# # Add time data
# df['DT'] = 15./60./24.

# # Load the tariffs data
# tariffs = pd.read_excel('INFO/TARIFAS.xlsx', sheet_name='TARIFAS')

# # Return the weekly and daily tariff for some timestamp
# count = 1
# def get_tariff(timestamp:pd.Timestamp):
# 	global count
# 	print("\rProgress:  {:6}/{} \t {} ".format(count, N, timestamp) , end='')
# 	count += 1

# 	def get_season(timestamp:pd.Timestamp):
# 		if 5 < timestamp.month < 11:
# 			return 'SUMMER'
# 		else:
# 			return 'WINTER'

# 	# Get necessary datetime properties
# 	date = timestamp.date()
# 	time = timestamp.time()
# 	weekday = timestamp.day_name()
# 	season = get_season(timestamp)
	
# 	# Make a filter
# 	selec = tariffs[
# 		(tariffs.SEASON.str.contains(season, case=False)) & 
# 		(tariffs.WEEKDAY.str.contains(weekday, case=False)) & 
# 		(tariffs.START <= time) & 
# 		(time <= tariffs.END)
# 	].set_index('CYCLE')

# 	# Validate size of result
# 	if len(selec) != 2:
# 		raise ValueError(f"Tariff calculation failed for the timestamp: {timestamp} ")

# 	# Return pandas series
# 	return pd.Series([selec.loc['WEEKLY', 'PERIOD'], selec.loc['DAILY', 'PERIOD']])


# # Determine the tariffs
# N = len(df)
# print(f"Number of tariffs to calculate: {N} ")
# df[['WEEKLY', 'DAILY']] = df['DATETIME'].apply(get_tariff)
# print('')

# # Create two separate sheets, pivoting by date
# df['DATE'] = df['DATETIME'].dt.date

# # Generate separate results for weekly and daily cycles
# df_weekly = df.copy()
# df_weekly.drop(['DATETIME', 'DAILY'], axis=1, inplace=True)
# df_weekly.rename(columns={"WEEKLY": "PERIOD"}, inplace=True)

# df_daily = df.copy()
# df_daily.drop(['DATETIME', 'WEEKLY'], axis=1, inplace=True)
# df_daily.rename(columns={"DAILY": "PERIOD"}, inplace=True)

# # Save to excel as pivot tables
# with pd.ExcelWriter("DATA/CORRECTED/consumos.xlsx") as writer:
# 	pd.pivot_table(df_weekly, values=['DT', 'kWh'], index=['DATE', 'PERIOD'], aggfunc=np.sum).reset_index().to_excel(writer, sheet_name="WEEKLY", index=False)
# 	pd.pivot_table(df_daily, values=['DT', 'kWh'], index=['DATE', 'PERIOD'], aggfunc=np.sum).reset_index().to_excel(writer, sheet_name="DAILY", index=False)





