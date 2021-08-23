import pandas as pd
from pathlib import Path
import sqlite3
from sqlite3 import Connection

from pandas.core.frame import DataFrame
import streamlit as st
import matplotlib.pyplot as plt
import datetime 
from sklearn.preprocessing import MinMaxScaler
import seaborn as sns
from setup import MODELS

URI_SQLITE_DB = "./data/pythonsqlite.db"

def main():
    st.title("KRS Water Level Forecasting")
    
    conn = get_connection(URI_SQLITE_DB)

    display_weather_data(conn)
    display_correlation(conn)
    display_forecast(conn)


def display_weather_data(conn : Connection):
    df = pd.read_sql("SELECT * FROM weather where location == 'karnataka'", con=conn)
    req = df.set_index(pd.to_datetime(df['date']))
    map_param = {'Maximum Temperature ': 'max_temp', 'Visibility': 'visibility','Cloud Cover': 'cloudcover','Humidity': 'humidity','View All': ['max_temp','visibility','cloudcover','humidity']}
    weather_selected = st.selectbox("Please select the weather parameter for which you would like to view weather data ",
                     map_param.keys())

    weather_param = map_param.get(weather_selected)
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

    st.write('Showing details for',weather_selected)



    fig, ax = plt.subplots(figsize=(15,8)) 
    req[weather_param].plot(ax =ax, colormap = 'Dark2',subplots = True)
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
    fig, ax = plt.subplots(figsize=(8,8)) 
    sns.heatmap(cor, xticklabels=cor.columns, yticklabels=cor.columns, annot=True,ax = ax)
    st.pyplot(fig)

def display_forecast(conn: Connection):
    actual = pd.read_sql("select date, storage_tmc from water where reservoir='krs'", con=conn)
    pred = pd.read_sql("select date, model, storage_tmc from water_forecast",con = conn)
    modeltitles = [x['title'] for x in MODELS]
    model_selected = st.selectbox("Select model", modeltitles)
    
    model = [item['number'] for item in MODELS if item['title'] == model_selected][0]
    pred = pred[pred['model']==model]

    last_n_days = display_model_info(model_selected)

    if st.checkbox("Display last " +  str(last_n_days) + " days prediction data"):
        st.dataframe(pred[-last_n_days:])

    actual['date'] = pd.to_datetime(actual['date'])
    pred['date'] = pd.to_datetime(pred['date'])
    pred['storage_tmc_prediction'] = pred['storage_tmc']
    pred.drop(columns = ['storage_tmc','model'],inplace=True)

    df = pd.merge(actual, pred, on = 'date', how = 'outer')
    df.set_index('date',inplace = True)
    

    if st.checkbox('Display monthly forecast plot for selected year'):
            forecast_year = st.slider("Select Year",2019,2021)
            input_date = str(forecast_year)
            if st.checkbox('Check box to further zoom into selected month'):

                forecast_month = st.slider("Select Month",1,12)


                if forecast_month <10:
                    input_date = str(forecast_year) + '-' + '0' +  str(forecast_month)
                else:
                    input_date = str(forecast_year) + '-' + str(forecast_month)
            df = df.loc[input_date]
            df = weekly_plot(df)
            
            
    

    fig, ax = plt.subplots(figsize=(15,7)) 
    df.plot(ax =ax, subplots = False,colormap = 'Dark2')
    plt.axhline(y=49.45, color='r', linestyle='--',label = 'Full Capacity of Dam Reached')
    ax.axhspan(49.45, 49.45-2, alpha=0.2, color='red')
    plt.axhline(y=4.4, color='black', linestyle='--',label = 'Dead Storage')
    ax.axhspan(4.4, 4.4+2, alpha=0.2, color='black')
    plt.plot()
    plt.legend()
    plt.autoscale()
    st.pyplot(fig)
   
def weekly_plot(df:DataFrame):
    plot_type_selected = st.selectbox("Please select graph type", ['Daily Forecast','Average Weekly Forecast'])
    if (plot_type_selected == 'Daily Forecast'):
        pass 
    if(plot_type_selected == 'Average Weekly Forecast'):
        df = df.resample('W-Mon').mean()
    return df

    
def display_model_info(model_selected):
    #st.write("Creating a space to insert information or static images. Just for demo")
    details = [item for item in MODELS if item['title'] == model_selected][0]
    for key,value in details.items():
        if key.lower() not in ['t', 'folder', 'horizon', 'reservoir', 'number', 'title']:
            st.markdown('**'+str(key).capitalize() + '** : '+ str(value))
    preds = details.get('HORIZON')
    return(preds)
    


@st.cache(hash_funcs={Connection: id})
def get_connection(path: str):
    """Put the connection in cache to reuse if path does not change between Streamlit reruns.
    NB : https://stackoverflow.com/questions/48218065/programmingerror-sqlite-objects-created-in-a-thread-can-only-be-used-in-that-sa
    """
    return sqlite3.connect(path, check_same_thread=False)

if __name__ == "__main__":
    main()
