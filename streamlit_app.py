import pandas as pd
from pathlib import Path
import sqlite3
from sqlite3 import Connection
import streamlit as st
import matplotlib.pyplot as plt
import datetime 

URI_SQLITE_DB = "data\\pythonsqlite.db"

def main():
    st.title("KRS Water Level Forecasting")
    #st.markdown("Enter data in database from sidebar, then run the **mighty** calculator")
    
    conn = get_connection(URI_SQLITE_DB)

    display_weather_data(conn)


def display_weather_data(conn : Connection):
    df = pd.read_sql("SELECT * FROM weather where location == 'karnataka'", con=conn)
    weather_param = st.sidebar.selectbox("Please select the weather parameter for which you would like to view weather data ",
                     ['min_temp', 'max_temp'])
    year = st.sidebar.slider("Year",2011,2020)
    month = st.sidebar.slider("Month",1,12)
    if month <10:
        input_date = str(year) + '-' + '0' +  str(month)
    else:
        input_date = str(year) + '-' + str(month)

    st.write('Showing details for',weather_param)

    req = df.set_index(pd.to_datetime(df['date']))
    req = req.loc[input_date]
    fig, ax = plt.subplots(figsize=(15,10)) 
    req[weather_param].plot(ax =ax, colormap = 'Dark2')
    st.pyplot(fig)
    if st.checkbox('show full data'):
        st.dataframe(req[weather_param])


@st.cache(hash_funcs={Connection: id})
def get_connection(path: str):
    """Put the connection in cache to reuse if path does not change between Streamlit reruns.
    NB : https://stackoverflow.com/questions/48218065/programmingerror-sqlite-objects-created-in-a-thread-can-only-be-used-in-that-sa
    """
    return sqlite3.connect(path, check_same_thread=False)

if __name__ == "__main__":
    main()


    

