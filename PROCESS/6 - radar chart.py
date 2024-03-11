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




# df = px.data.wind()
# fig = px.scatter_polar(df, r="frequency", theta="direction")
# fig.show()

#fig=px.line(x=[1,2,3,4],y=[1,4,9,16])
# fig = px.line_polar(r=[1,2,3], theta=[1,2,3])#, line_close=True)
# fig.show(renderer='vscode')

import plotly.graph_objs as go
from plotly.offline import iplot


# fig = px.line_polar(pvt, r='kWh', theta='TIME', line_close=True)
# fig.update_traces(fill='toself')
# iplot([fig])

# table = ff.create_table(df.head())
# py.iplot(table, filename='jupyter-table1')

# pvt = pd.pivot_table(
#     data=df,
#     values='kWh',
#     index=['MONTH', 'HOUR'],
#     columns='YEAR',
#     aggfunc='sum'
# )
# sns.lineplot(pvt.loc[(10), 2022])
# sns.lineplot(pvt.loc[(10), 2023])