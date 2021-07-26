import pandas as pd
from pathlib import Path
import sqlite3
from sqlite3 import Connection
import streamlit as st
import matplotlib.pyplot as plt
import datetime 
from sklearn.preprocessing import MinMaxScaler
import seaborn as sns

URI_SQLITE_DB = "data\\pythonsqlite.db"

def main():
    st.title("KRS Water Level Forecasting")
    
    conn = get_connection(URI_SQLITE_DB)

    display_weather_data(conn)
    display_correlation(conn)


def display_weather_data(conn : Connection):
    df = pd.read_sql("SELECT * FROM weather where location == 'karnataka'", con=conn)
    req = df.set_index(pd.to_datetime(df['date']))
    weather_param = st.selectbox("Please select the weather parameter for which you would like to view weather data ",
                     ['min_temp', 'max_temp'])

    if st.checkbox('Display monthly plot for selected year'):
        year = st.slider("Year",2011,2020)
        input_date = str(year)
        if st.checkbox('Display daily data for selected month'):

            month = st.slider("Month",1,12)


            if month <10:
                input_date = str(year) + '-' + '0' +  str(month)
            else:
                input_date = str(year) + '-' + str(month)
        req = req.loc[input_date]

    st.write('Showing details for',weather_param)



    fig, ax = plt.subplots(figsize=(15,10)) 
    req[weather_param].plot(ax =ax, colormap = 'Dark2')
    st.pyplot(fig)
    if st.checkbox('show full data'):
        st.dataframe(req[weather_param])

def display_correlation(conn : Connection):
    wtr = pd.read_sql("SELECT date,max_temp,visibility,cloudcover,humidity FROM weather where location == 'karnataka'", con=conn)
    krs = pd.read_sql("SELECT  date, inflow_cusecs, outflow_cusecs, storage_tmc FROM water where reservoir == 'krs'", con=conn)

    krs['Date'] = pd.to_datetime(krs['date'])
    wtr['Date'] = pd.to_datetime(wtr['date'])
    df = krs.merge(wtr)
    df.drop(columns=['Date','date'],inplace = True)
    index_names = df[ df['inflow_cusecs'] == '&nbsp;' ].index
    df.drop(index_names, inplace = True)
    mms = MinMaxScaler()
    df = pd.DataFrame(mms.fit_transform(df),columns = df.columns)
    st.write("HeatMap for correlation between various features of data collected")
    #heatmap for normalised data
    cor = df.corr()
    fig, ax = plt.subplots(figsize=(10,10)) 
    sns.heatmap(cor, xticklabels=cor.columns, yticklabels=cor.columns, annot=True,ax = ax)
    st.pyplot(fig)




@st.cache(hash_funcs={Connection: id})
def get_connection(path: str):
    """Put the connection in cache to reuse if path does not change between Streamlit reruns.
    NB : https://stackoverflow.com/questions/48218065/programmingerror-sqlite-objects-created-in-a-thread-can-only-be-used-in-that-sa
    """
    return sqlite3.connect(path, check_same_thread=False)

if __name__ == "__main__":
    main()
