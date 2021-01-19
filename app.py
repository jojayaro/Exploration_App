import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


'''
# AER ST1 Well Licences Locations by Operator

This is a test site please contact me at **jayaro@gmail.com** for more information.
'''
#Open ST1 data
data = pd.read_csv('ST1.csv')

#Create Dropdown by Licensee
licensee = data.LICENSEE.unique()
option = st.selectbox('Select Operator from the list below to update locations', sorted(licensee))
filter_data = data[data['LICENSEE'] == option]

#Map from selected Licensee
st.map(filter_data)

'''
---
## Data for selected Operator

'''
#Dataframe showing filtered data from selected Licensee
st.dataframe(filter_data.sort_values(by='WEEK'))

'''
---
# Weekly Activity (2020)

Licenses issued by week broken down by substance (for all operators)
'''
df = data[data['YEAR'] == 2020]

#Data Cleaning for Weekly Data
df = pd.pivot_table(df, index=['WEEK'], columns=['SUBSTANCE'], values=['LICENSEE'], aggfunc='count')
df.columns = df.columns.droplevel(0)
df = df.rename_axis(None, axis=1)
if isinstance(df, (pd.DatetimeIndex, pd.MultiIndex)):
	df = df.to_frame(index=False)

#Remove any pre-existing indices for ease of use in the D-Tale code, but this is not required
df = df.reset_index().drop('index', axis=1, errors='ignore')
df.columns = [str(c) for c in df.columns]  # update columns to strings in case they are numbers

chart_data = pd.concat([
	df['WEEK'],
	df['CRUDE OIL'],
	df['CRUDE BITUMEN'],
	df['GAS'],
], axis=1)
chart_data = chart_data.sort_values(['WEEK'])
chart_data = chart_data.rename(columns={'WEEK': 'x'})
chart_data = chart_data.dropna()

#Plotly Graph

fig = go.Figure()
fig.add_trace(go.Scatter(x=chart_data['x'], y=chart_data['CRUDE OIL'],
                    mode='lines',
                    name='Crude Oil'))
fig.add_trace(go.Scatter(x=chart_data['x'], y=chart_data['GAS'],
                    mode='lines',
                    name='Gas'))
fig.add_trace(go.Scatter(x=chart_data['x'], y=chart_data['CRUDE BITUMEN'],
                    mode='lines', name='Crude Bitumen'))

st.plotly_chart(fig)