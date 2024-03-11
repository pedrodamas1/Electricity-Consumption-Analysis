
import pandas as pd 
import numpy as np 


df_weekly = pd.read_excel('DATA/consumos.xlsx', sheet_name='WEEKLY')
df_daily = pd.read_excel('DATA/consumos.xlsx', sheet_name='DAILY')


#   EREDES
df_weekly_eredes = df_weekly.copy()
df_weekly_eredes['YEAR'] = df_weekly_eredes['DATE'].dt.year
df_weekly_eredes['MONTH'] = df_weekly_eredes['DATE'].dt.month
#df_weekly_eredes['MONTH'] = df_weekly_eredes['DATE'].dt.month_name()

df_daily_eredes = df_daily.copy()
df_daily_eredes['YEAR'] = df_daily_eredes['DATE'].dt.year
df_daily_eredes['MONTH'] = df_daily_eredes['DATE'].dt.month
#df_daily_eredes['MONTH'] = df_daily_eredes['DATE'].dt.month_name()

#   SUMMATION
with pd.ExcelWriter("DATA/resumo_eRedes.xlsx") as writer:
	pd.pivot_table(df_weekly_eredes, values=['kWh'], index=['YEAR', 'MONTH'], columns=['PERIOD'], aggfunc=np.sum).reset_index().to_excel(writer, sheet_name="WEEKLY")
	pd.pivot_table(df_daily_eredes, values=['kWh'], index=['YEAR', 'MONTH'], columns=['PERIOD'], aggfunc=np.sum).reset_index().to_excel(writer, sheet_name="DAILY")


#   EREDES
df_weekly_gold = df_weekly.copy()
df_weekly_gold['DATE'] = df_weekly_gold['DATE'] - pd.DateOffset(days=21) + pd.DateOffset(months=1)
df_weekly_gold['YEAR'] = df_weekly_gold['DATE'].dt.year
df_weekly_gold['MONTH'] = df_weekly_gold['DATE'].dt.month
#df_weekly_eredes['MONTH'] = df_weekly_eredes['DATE'].dt.month_name()

df_daily_gold = df_daily.copy()
df_daily_gold['DATE'] = df_daily_gold['DATE'] - pd.DateOffset(days=21) + pd.DateOffset(months=1)
df_daily_gold['YEAR'] = df_daily_gold['DATE'].dt.year
df_daily_gold['MONTH'] = df_daily_gold['DATE'].dt.month
#df_daily_eredes['MONTH'] = df_daily_eredes['DATE'].dt.month_name()

#   SUMMATION
with pd.ExcelWriter("DATA/resumo_goldEnergy.xlsx") as writer:
	pd.pivot_table(df_weekly_gold, values=['kWh'], index=['YEAR', 'MONTH'], columns=['PERIOD'], aggfunc=np.sum).reset_index().to_excel(writer, sheet_name="WEEKLY")
	pd.pivot_table(df_daily_gold, values=['kWh'], index=['YEAR', 'MONTH'], columns=['PERIOD'], aggfunc=np.sum).reset_index().to_excel(writer, sheet_name="DAILY")



# import pandas as pd 
# import numpy as np 

# # Load our semi-crunched data
# df = pd.read_excel('PROCESS/RAW.xlsx')

# # Add important data
# df['DATETIME'] = df['DATETIME'] - pd.DateOffset(days=21) + pd.DateOffset(months=1)
# df['YEAR'] = df['DATETIME'].dt.year
# df['MONTH'] = df['DATETIME'].dt.month_name()
# df['kWh'] = df['kW'] * 15./60
# df['DT'] = 15./60./24.

# df = pd.melt(df, id_vars=['YEAR', 'MONTH', 'kWh', 'DT'], var_name='CYCLE', value_vars=['WEEKLY', 'DAILY'], value_name='PERIOD')
# df = pd.pivot_table(df, values=['DT', 'kWh'], index=['YEAR', 'MONTH', 'CYCLE', 'PERIOD'], aggfunc=np.sum)
# df.reset_index().to_excel('PROCESS/SUMMARY_ASYNC.xlsx', index=False)





# '''
# The aim of this script, assuming WEEKLY scheme is to:
# 1) calculate the cost of each kWh entry for each suplier/scheme
# 2) Calculate the total cost for each SUPPLIER offer
# '''

# import pandas as pd 

# # Load our semi-crunched data
# df_prices = pd.read_excel('PROCESS/PREÇOS.xlsx', sheet_name='PREÇOS')
# pacotes = (df_prices['SUPPLIER'] + ' ' + df_prices['TARIFF']).values
# df_prices.set_index(['SUPPLIER', 'TARIFF'], inplace=True)
# df_kwh = pd.read_excel('PROCESS/SUMMARY_ASYNC.xlsx')



# def get_price(data, *args):
#     KVA, VAZIO, CHEIAS, PONTA, DIARIO, _ = args
#     cost = data.DT * DIARIO
#     if data.PERIOD == 'VAZIO':
#         return cost + data.kWh * VAZIO
#     elif data.PERIOD == 'CHEIAS':
#         return cost + data.kWh * CHEIAS
#     elif data.PERIOD == 'PONTA':
#         return cost + data.kWh * PONTA
#     else:
#         raise ValueError('Please check the values.')
    
# for index, row in df_prices.iterrows():
#     col = ' '.join(index)
#     df_kwh[col] = df_kwh[['PERIOD', 'DT', 'kWh']].apply(get_price, args=tuple(row.values), axis=1)


# df_kwh = pd.melt(df_kwh, id_vars=['YEAR', 'MONTH', 'CYCLE', 'PERIOD', 'kWh', 'DT'], var_name='PACOTES', value_vars=pacotes, value_name='COST')
# df_kwh.to_excel('PROCESS/custos.xlsx', index=False)
