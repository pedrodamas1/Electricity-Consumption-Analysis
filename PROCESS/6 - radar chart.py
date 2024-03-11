'''
This script plots a radar chart of our average daily hourly consumption
'''

import pandas as pd 
import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_excel('DATA/CRUNCHED/Consumos DAILY.xlsx')

ax = sns.lineplot(pd.pivot_table(data=df, values='kWh', index='DATE', columns='PERIOD').cumsum())
ax.grid()
plt.show()


# df = pd.read_excel('DATA/ASSIGNED/Consumos MINUTO.xlsx')

# import plotly.express as px

# 
# df['HOUR'] = df['DATETIME'].dt.hour
# pvt = pd.pivot_table(df, values=['kWh'], index=['TIME'], aggfunc='mean').reset_index()


# #pvt = pd.pivot_table(df, values=['kWh'], index=['HOUR'], aggfunc=np.average).reset_index()
# #pvt['HOUR'] = pvt['HOUR'].apply(str)

# #fig = px.line_polar(pvt, r='kWh', theta='HOUR', line_close=True)
# fig = px.line_polar(pvt, r='kWh', theta='TIME', line_close=True)
# fig.update_traces(fill='toself')
# fig.show()
