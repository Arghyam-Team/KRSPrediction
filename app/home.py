import pandas as pd
from pandas.core.tools.datetimes import to_datetime
#from pathlib import Path
#import sqlite3
#from sqlite3 import Connection

#from pandas.core.frame import DataFrame
import streamlit as st
#import matplotlib.pyplot as plt
import datetime 
#from sklearn.preprocessing import MinMaxScaler
#import seaborn as sns
from setup import MODELS
from connection_setup import CONN
#from help import PredictionsHelp
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import plotly.express as px
import plotly.graph_objects as go


class Home:
    def __init__(self):
        self.image_file = "../Images/home-legend.png"
        self.type_select = st.sidebar.radio("Select Display",['Monthly','Weekly','Daily'])
        st.sidebar.image(self.image_file,caption = 'Legend for map',width = 200)
        self.actual = pd.read_sql("select date, storage_tmc from water where reservoir='krs'", con=CONN)
        self.pred = pd.read_sql("select date, model, storage_tmc from water_forecast",con = CONN)
        self.weather = pd.read_sql("SELECT * FROM weather where location == 'karnataka'", con=CONN)

        self.actual['date'] = pd.to_datetime(self.actual['date'])
        self.pred['date'] = pd.to_datetime(self.pred['date'])
        self.weather['date'] = pd.to_datetime(self.weather['date'])
        self.pred['storage_tmc_pred'] = self.pred['storage_tmc']
        self.pred['storage_tmc_pred_pct'] = self.pred['storage_tmc_pred']/50*100
        self.actual['storage_tmc_pct'] = self.actual['storage_tmc']/50*100
        self.pred = self.pred.sort_values(by = 'date')
        self.pred = self.pred[self.pred['model']== 12]
        self.pred.drop(columns = ['storage_tmc','model'],inplace=True)
        self.df = pd.merge(self.actual, self.pred, on = 'date', how = 'outer')
        self.df = pd.merge(self.df, self.weather, on = 'date', how = 'outer')

        self.df = self.df.set_index(pd.to_datetime(self.df['date']))

        file1 = open("../lastupdatedon.txt","r")
        self.today = file1.read()
        self.td = datetime.fromisoformat(self.today)
        

        if self.type_select == 'Monthly':
            self.monthly()
        elif self.type_select == 'Weekly':
            self.weekly()
        else:
            self.daily()

        st.write("Last updated on", self.today)

    def monthly(self):
        self.df1 = self.df.resample('M').mean()
        self.time_paramter1 = 'this month (Mean)'
        self.time_paramter2 = 'last month'
        #st.dataframe(self.df1)
        self.current_year_month = "-".join(self.today.split('-')[:-1])
        self.metric_dataframe = self.df1.loc[self.current_year_month]
        last = str(self.td - relativedelta(months=+1))
        last_year_month = "-".join(last.split('-')[:-1])
        self.since_last_dataframe = self.df1.loc[last_year_month]
        #st.dataframe(self.since_last_dataframe)
        self.display_metric()
       

        #st.write("done",self.current_year_month)

        self.start_date = str(self.td - relativedelta(months=+5))
        self.end_date = str(self.td + relativedelta(months=+2))

        #start_date_month = "-".join(self.start_date.split('-')[:-1])
        #end_date_month = "-".join(self.end_date.split('-')[:-1])

        self.df1 = self.df1.reset_index()

        actual_mask = (self.df1['date'] >= self.start_date) & (self.df1['date'] <= self.today)
        pred_mask = (self.df1['date'] >= self.start_date) & (self.df1['date'] <= self.end_date)


        fig = go.Figure()
        fig.add_trace(go.Scatter(x=self.df1[['storage_tmc_pct','date']].loc[actual_mask].date, y=self.df1[['storage_tmc_pct','date']].loc[actual_mask].storage_tmc_pct, fill='tozeroy',mode = 'markers',line_color = 'blue',name = 'Storage Values',showlegend = False ))

        fig.add_trace(go.Scatter(x=self.df1[['storage_tmc_pred_pct','date']].loc[pred_mask].date, y=self.df1[['storage_tmc_pred_pct','date']].loc[pred_mask].storage_tmc_pred_pct, fill='tozeroy',mode = 'markers',line_color = 'royalblue',name = 'Predictions',showlegend = False))

        
        fig.update_layout(height = 380, width = 800,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="LightSteelBlue",
        yaxis_title="Storage in Percentage",
        xaxis_title="Date",
        )
        
        st.plotly_chart(fig)

        
        #self.year_month = self.today - self.today.split('-')
        #st.write(self.year_month)
        #st.dataframe(self.df1.loc[self.df1.index.month == month])
        
        #self.td = self.td - datetime.timedelta(days=-self.td.weekday(), weeks=1)

    def weekly(self):
        self.df2 = self.df.resample('W-Mon').mean()
        #st.dataframe(self.df2)
        self.time_paramter1 = 'this week (Mean)'
        self.time_paramter2 = 'last week'
        #st.dataframe(self.df1)
        def nearest(items, pivot):
            return min(items, key=lambda x: abs(x - pivot))
        self.current_week = str(nearest(self.df2.index,self.td))
        #st.write("This week",self.current_week)
        self.metric_dataframe = self.df2.loc[str(self.current_week)]
        last_week =  str(nearest(self.df2.index,self.td-timedelta(weeks=1)))                                         
        self.since_last_dataframe = self.df2.loc[last_week]
        #st.dataframe(self.since_last_dataframe)
        self.display_metric()
       

        #st.write("done",self.current_year_month)

        self.start_date = str(nearest(self.df2.index,self.td-timedelta(weeks=7)))
        self.end_date = str(nearest(self.df2.index,self.td+timedelta(weeks=5)))

        #start_date_month = "-".join(self.start_date.split('-')[:-1])
        #end_date_month = "-".join(self.end_date.split('-')[:-1])

        self.df2 = self.df2.reset_index()

        actual_mask = (self.df2['date'] >= self.start_date) & (self.df2['date'] <= self.today)
        pred_mask = (self.df2['date'] >= self.start_date) & (self.df2['date'] <= self.end_date)


        fig = go.Figure()
        fig.add_trace(go.Scatter(x=self.df2[['storage_tmc_pct','date']].loc[actual_mask].date, y=self.df2[['storage_tmc_pct','date']].loc[actual_mask].storage_tmc_pct, fill='tozeroy',mode = 'markers',line_color = 'blue',name = 'Storage Values',showlegend = False  ))

        fig.add_trace(go.Scatter(x=self.df2[['storage_tmc_pred_pct','date']].loc[pred_mask].date, y=self.df2[['storage_tmc_pred_pct','date']].loc[pred_mask].storage_tmc_pred_pct, fill='tozeroy',mode = 'markers',line_color = 'royalblue',name = 'Predictions',showlegend = False ))

        
        fig.update_layout(height = 350, width = 800,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="LightSteelBlue",
        yaxis_title="Storage in Percentage",
        xaxis_title="Date",
        )
        
        st.plotly_chart(fig)

    def daily(self):
        #st.dataframe(self.df2)
        self.time_paramter1 = 'today'
        self.time_paramter2 = 'yesterday'
        #st.dataframe(self.df1)
        #st.write("This week",self.current_week)
        self.metric_dataframe = self.df.loc[self.today]
        yesterday =  str(self.td-timedelta(days=1))                                    
        self.since_last_dataframe = self.df.loc[yesterday]
        #st.dataframe(self.since_last_dataframe)
        self.display_metric()
       

        #st.write("done",self.current_year_month)

        self.start_date = str(self.td-timedelta(days=7))
        self.end_date = str(self.td + timedelta(days=7))

        #start_date_month = "-".join(self.start_date.split('-')[:-1])
        #end_date_month = "-".join(self.end_date.split('-')[:-1])

        #self.df = self.df.reset_index()

        actual_mask = (self.df['date'] >= self.start_date) & (self.df['date'] <= self.today)
        pred_mask = (self.df['date'] >= self.start_date) & (self.df['date'] <= self.end_date)


        fig = go.Figure()
        fig.add_trace(go.Scatter(x=self.df[['storage_tmc_pct','date']].loc[actual_mask].date, y=self.df[['storage_tmc_pct','date']].loc[actual_mask].storage_tmc_pct, fill='tozeroy',mode = 'markers',line_color = 'blue',name = 'Storage Values', showlegend = False  ))

        fig.add_trace(go.Scatter(x=self.df[['storage_tmc_pred_pct','date']].loc[pred_mask].date, y=self.df[['storage_tmc_pred_pct','date']].loc[pred_mask].storage_tmc_pred_pct, fill='tozeroy',mode = 'markers',line_color = 'royalblue',name = 'Predictions',showlegend = False ))

        
        fig.update_layout(height = 350, width = 800,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="LightSteelBlue",
        yaxis_title="Storage in Percentage",
        xaxis_title="Date",
        )
        
        st.plotly_chart(fig)



    def display_metric(self):
        #st.dataframe(self.metric_dataframe)
        #st.write("Storage TMC",self.metric_dataframe.storage_tmc)
        try:
            self.today_metric = self.metric_dataframe.storage_tmc.values[0]
            self.changeSinceLastValue = self.since_last_dataframe.storage_tmc.values[0]
            self.visibility = self.metric_dataframe.visibility.values[0]
            self.max_temperature = self.metric_dataframe.max_temp.values[0]
            self.wind = self.metric_dataframe.wind.values[0]
        except:
            self.today_metric = self.metric_dataframe.storage_tmc
            self.changeSinceLastValue = self.since_last_dataframe.storage_tmc
            self.visibility = self.metric_dataframe.visibility
            self.max_temperature = self.metric_dataframe.max_temp
            self.wind = self.metric_dataframe.wind
        
        self.today_display = self.today_metric/50*100
        #st.dataframe(self.since_last_dataframe)
        #st.write("Change since last",self.time_paramter,self.df.)
        self.label = "Storage " + self.time_paramter1
        col1,col2,col3,col4 = st.columns([5,2,4,2])
        col1.metric(label=self.label, value=str(round(self.today_display,1))+'%',delta = str(round((self.today_metric-self.changeSinceLastValue)/50*100,1))+'%'+' Change since '+ self.time_paramter2)
        col2.metric(label = 'Visibility (Kms)', value = round(self.visibility,1))
        col3.metric(label = "Maximum Temperature (Celsius)", value = round(self.max_temperature,1))
        col4.metric(label = "Wind", value = round(self.wind,1))
        
