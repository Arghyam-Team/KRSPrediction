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
from datetime import date, timedelta
import plotly.express as px
import plotly.graph_objects as go

class Home:
    def __init__(self):
 
        self.type_select = st.sidebar.radio("Select Display",['Daily','Weekly'])
   
        self.daily()

    
        
        
        

    def daily(self):
        #st.write(self.today)
        self.actual = pd.read_sql("select date, storage_tmc from water where reservoir='krs'", con=CONN)
        self.pred = pd.read_sql("select date, model, storage_tmc from water_forecast",con = CONN)
        self.actual['date'] = pd.to_datetime(self.actual['date'])
        self.pred['date'] = pd.to_datetime(self.pred['date'])
        self.pred = self.pred.sort_values(by = 'date')

        self.pred = self.pred[self.pred['model']== 13]

        self.td  = datetime.date(2021, 7, 29)
        st.write(self.td)
        self.today = str(self.td)
        self.actual = self.actual.set_index('date')
        self.pred = self.pred.set_index('date')
        if self.type_select == 'Weekly':
            st.dataframe(self.actual)
            self.weekly()
        self.today_metric = self.actual.loc[self.today].values[0][0]
        self.today_display = self.today_metric/50*100
        self.yd = str(self.td - timedelta(days=1))
        self.yesterday_value = self.actual.loc[self.yd].values[0][0]
        st.metric(label="Storage Today in TMC", value=str(round(self.today_display,1))+'%',delta = str(round((self.today_metric-self.yesterday_value)/50*100,1))+'%')


        self.start_date = str(self.td - timedelta(days=5))
        self.end_date = str(self.td + timedelta(days = 5))

   
        
        self.actual.reset_index(inplace = True)
        self.pred.reset_index(inplace = True)

            

        actual_mask = (self.actual['date'] >= self.start_date) & (self.actual['date'] <= self.today)
        pred_mask = (self.pred['date'] >= self.start_date) & (self.pred['date'] <= self.end_date)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=self.actual.loc[actual_mask].date, y=self.actual.loc[actual_mask].storage_tmc, fill='tozeroy',mode = 'markers',line_color = 'blue',name = 'Storage Values'  ))

        fig.add_trace(go.Scatter(x=self.pred.loc[pred_mask].date, y=self.pred.loc[pred_mask].storage_tmc, fill='tozeroy',mode = 'markers',line_color = 'royalblue',name = 'Predictions' ))

        #fig.add_trace(go.Scatter(x=self.actual.loc[self.today].date, y=self.actual.loc[self.today].storage_tmc,mode = 'markers',line_color = 'red',name = 'Today'  ))

        

        fig.update_layout(height = 400, width = 1100,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="LightSteelBlue",
        )
        
        st.plotly_chart(fig)

    """def weekly(self):
        self.actual.set_index('date',inplace = True)
        self.pred.set_index('date',inplace = True)
        self.actual = self.actual.resample('W-Mon').mean()
        self.pred = self.pred.resample('W-Mon').mean()
        self.today = self.today - datetime.timedelta(days=-self.today.weekday(), weeks=1)
        self.today_metric = self.actual.loc[self.today].get(0)
        self.today_display = self.today_metric/50*100
        self.yd = str(self.td - timedelta(days=1))
        self.yesterday_value = self.actual.loc[self.yd].get(0)
        st.metric(label="Storage Today in TMC", value=str(round(self.today_display,1))+'%',delta = str(round((self.today_metric-self.yesterday_value)/50*100,1))+'%')


        self.start_date = str(self.td - timedelta(weeks=5))
        self.end_date = str(self.td + timedelta(weeks = 5))
        self.actual.reset_index(inplace = True)
        self.pred.reset_index(inplace = True)

        actual_mask = (self.actual['date'] >= self.start_date) & (self.actual['date'] <= self.today)
        pred_mask = (self.pred['date'] >= self.start_date) & (self.pred['date'] <= self.end_date)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=self.actual.loc[actual_mask].date, y=self.actual.loc[actual_mask].storage_tmc, fill='tozeroy',mode = 'markers',line_color = 'blue',name = 'Storage Values'  ))

        fig.add_trace(go.Scatter(x=self.pred.loc[pred_mask].date, y=self.pred.loc[pred_mask].storage_tmc, fill='tozeroy',mode = 'markers',line_color = 'royalblue',name = 'Predictions' ))

        
"""
    def weekly(self):
        self.actual = self.actual.resample('W-Mon').mean()
        self.pred = self.pred.resample('W-Mon').mean()
        self.td = self.td - datetime.timedelta(days=-self.td.weekday(), weeks=1)
        self.today = str(self.td)
        self.today_metric = self.actual.loc[self.today].values[0][0]
        #self.today_display = self.today_metric/50*100
        #self.yd = str(self.td - timedelta(weeks=1))
        #self.yesterday_value = self.actual.loc[self.yd].get(0)
        #st.metric(label="Storage Today in TMC", value=str(round(self.today_metric,1))+'%',delta = str(round((self.today_metric-self.yesterday_value)/50*100,1))+'%')
        st.metric(label="Storage Today in TMC", value=str(round(self.today_metric,1))+'%')
        self.start_date = str(self.td - timedelta(weeks=1))
        self.end_date = str(self.td + timedelta(weeks = 1))
