'''
This script compares the monthly totals of the raw files with the corrected files.
'''

import pandas as pd 
import re 

# Generate a placeholder for data
data = pd.DataFrame(columns=['Year', 'Month', 'RAW', 'CORRECTED']).set_index(['Year', 'Month'])
# data.loc[('1', '2'),:] = 1,2
# data.loc[('1', '23'), 'RAW'] = 3

# List the folders for analysis
state = 'RAW'
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

    consumo = df['Consumo registado, Ativa'].sum() * 15/60
    data.loc[(year, month), 'RAW'] = consumo

# List the folders for analysis
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

    consumo = df['Consumo registado, Ativa'].sum() * 15/60
    data.loc[(year, month), 'CORRECTED'] = consumo

data.reset_index().to_excel('DATA/CORRECTED/Validação e-redes.xlsx', index=False)



