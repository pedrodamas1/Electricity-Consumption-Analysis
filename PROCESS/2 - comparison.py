'''
This script compares the monthly totals of the raw files with the corrected files.
'''

import pandas as pd 
import re 

# Generate a placeholder for data
data = pd.DataFrame(columns=['Year', 'Month', 'RAW', 'CORRECTED']).set_index(['Year', 'Month'])

# List the folders for analysis
paths = ['DATA/RAW/2022/{:02d}.xlsx'.format(month) for month in range(7,13)] + \
    ['DATA/RAW/2023/{:02d}.xlsx'.format(month) for month in range(1,13)]

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

    consumo = df['Consumo registado, Ativa'].sum() * 15/60
    data.loc[(year, month), 'RAW'] = consumo

# List the folders for analysis
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

    consumo = df['Consumo registado, Ativa'].sum() * 15/60
    data.loc[(year, month), 'CORRECTED'] = consumo

data.reset_index().to_excel('DATA/CORRECTED/Validação e-redes.xlsx', index=False)



