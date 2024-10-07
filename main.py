import streamlit as st
from streamlit_autorefresh import st_autorefresh
import requests
import pandas as pd
import datetime


endpoint = 'https://9zo6auku77.execute-api.sa-east-1.amazonaws.com/last_items'

try:
    data = requests.get(endpoint)

except Exception as e:
    st.title('Não foi possível recuperar os dados!')
    st.write(f'Houve um erro! {str(e)}')
    st.stop()


list_elements = data.json()

try:
    df = pd.DataFrame(list_elements)
    df.sort_values(['time'], inplace=True)
    df['time'] = pd.to_datetime(df['time'], unit='ms')

    last_heart_rate = df['heart_rate'].iloc[-1]
    last_spO2 = df['spO2'].iloc[-1]
    
except Exception as e:
    st.title('Não há dados disponíveis!')
    st.write(f'Houve um erro! {str(e)}')
    st.stop()

count = st_autorefresh(interval=5000, limit=15)

st.title(f'Health Data')
st.divider()

metric_col1, metric_col2 = st.columns(2)
metric_col1.metric('Heart rate', f'{last_heart_rate:.0f} bpm')
metric_col2.metric('SpO2', f'{last_spO2} %')
st.divider()

st.header('Heart rate history')
st.line_chart(df, x='time', y='heart_rate')
st.header('SpO2 history')
st.line_chart(df, x='time', y='spO2')
