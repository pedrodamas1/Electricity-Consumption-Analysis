'''
This script plots a radar chart of our average daily hourly consumption
'''

import pandas as pd 
import numpy as np 
import plotly.express as px

df = pd.read_excel('DATA/ASSIGNED/Consumos MINUTO.xlsx')
df['HOUR'] = df['DATETIME'].dt.hour

pvt = pd.pivot_table(df, values=['kWh'], index=['TIME'], aggfunc=np.average).reset_index()
#pvt = pd.pivot_table(df, values=['kWh'], index=['HOUR'], aggfunc=np.average).reset_index()
#pvt['HOUR'] = pvt['HOUR'].apply(str)

#fig = px.line_polar(pvt, r='kWh', theta='HOUR', line_close=True)
fig = px.line_polar(pvt, r='kWh', theta='TIME', line_close=True)
fig.update_traces(fill='toself')
fig.show()
