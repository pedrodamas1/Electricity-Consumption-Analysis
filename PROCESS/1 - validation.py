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


# List the folders for analysis.
# paths = ['DATA/RAW/2022/{:02d}.xlsx'.format(month) for month in range(7,13)] + \
#     ['DATA/RAW/2023/{:02d}.xlsx'.format(month) for month in range(1,13)]
paths = ['DATA/CORRECTED/2022/{:02d}.xlsx'.format(month) for month in range(7,13)] + \
    ['DATA/CORRECTED/2023/{:02d}.xlsx'.format(month) for month in range(1,13)]

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
