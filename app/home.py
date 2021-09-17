import pandas as pd
from pandas.core.tools.datetimes import to_datetime
#from pathlib import Path
#import sqlite3
#from sqlite3 import Connection
import numpy as np
#from pandas.core.frame import DataFrame
import streamlit as st
#import matplotlib.pyplot as plt
import datetime 
#from sklearn.preprocessing import MinMaxScaler
#import seaborn as sns
from connection_setup import CONN
#from help import PredictionsHelp
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import plotly.express as px
import plotly.graph_objects as go
from setup import MODELS, get_full_path
from PIL import Image 
#import statsmodels.api as sm

class Home:
    def __init__(self):
        self.image_file = Image.open(get_full_path("Images", "home-legend.png"))
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
        self.current_year_month = ""
        self.advise = ""

        self.df = self.df.set_index(pd.to_datetime(self.df['date']))

        file1 = open(get_full_path("lastupdatedon.txt"),"r")
        self.today = file1.read()
        self.td = datetime.fromisoformat(self.today)
        #self.weather_info = st.expander("Expand for more information")


        self.actual_mask_month = ""
        self.pred_mask_month = ""
        if self.type_select == 'Monthly':
            self.monthly()
        elif self.type_select == 'Weekly':
            self.weekly()
        else:
            self.daily()
        #self.summary()
        col1, col2 = st.columns([1,2])
        self.risk_advisory()
        col1.write("Last updated on " + self.today)
        col2.write(self.advise)

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
        self.end_date = str(self.td + relativedelta(months=+3))

        #start_date_month = "-".join(self.start_date.split('-')[:-1])
        #end_date_month = "-".join(self.end_date.split('-')[:-1])

        self.df1 = self.df1.reset_index()

        self.actual_mask_month = (self.df1['date'] >= self.start_date) & (self.df1['date'] <= self.today)
        self.pred_mask_month = (self.df1['date'] >= self.start_date) & (self.df1['date'] <= self.end_date)


        fig = go.Figure()
        fig.add_trace(go.Scatter(x=self.df1[['storage_tmc_pct','date']].loc[self.actual_mask_month].date, y=self.df1[['storage_tmc_pct','date']].loc[self.actual_mask_month].storage_tmc_pct, fill='tozeroy',mode = 'markers',line_color = 'blue',name = 'Storage Values',showlegend = False ))

        fig.add_trace(go.Scatter(x=self.df1[['storage_tmc_pred_pct','date']].loc[self.pred_mask_month].date, y=self.df1[['storage_tmc_pred_pct','date']].loc[self.pred_mask_month].storage_tmc_pred_pct, fill='tozeroy',mode = 'markers',line_color = 'royalblue',name = 'Predictions',showlegend = False))

        
        fig.update_layout(autosize=True,
        yaxis_title="Storage in Percentage",
        xaxis_title="Date",
        )
        #https://plotly.com/python/legend/
        summary_expander = st.expander("Expand for more info")
        with summary_expander:
            self.summary()
        st.plotly_chart(fig, use_container_width=True)
        

        
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

        
        fig.update_layout(autosize=True,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="LightSteelBlue",
        yaxis_title="Storage in Percentage",
        xaxis_title="Date",
        )
        
        st.plotly_chart(fig, use_container_width=True)

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
        pred_mask= (self.df['date'] >= self.start_date) & (self.df['date'] <= self.end_date)


        fig = go.Figure()
        fig.add_trace(go.Scatter(x=self.df[['storage_tmc_pct','date']].loc[actual_mask].date, y=self.df[['storage_tmc_pct','date']].loc[actual_mask].storage_tmc_pct, fill='tozeroy',mode = 'markers',line_color = 'blue',name = 'Storage Values', showlegend = False  ))

        fig.add_trace(go.Scatter(x=self.df[['storage_tmc_pred_pct','date']].loc[pred_mask].date, y=self.df[['storage_tmc_pred_pct','date']].loc[pred_mask].storage_tmc_pred_pct, fill='tozeroy',mode = 'markers',line_color = 'royalblue',name = 'Predictions',showlegend = False ))

        
        fig.update_layout(autosize=True,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="LightSteelBlue",
        yaxis_title="Storage in Percentage",
        xaxis_title="Date",
        )
        
        st.plotly_chart(fig, use_container_width=True)
        


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
        col1,col2,col3,col4 = st.columns([6,2,4,2])
        col1.metric(label=self.label, value=str(round(self.today_display,1))+'%',delta = str(round((self.today_metric-self.changeSinceLastValue)/50*100,1))+'%'+' Expected Change since '+ self.time_paramter2)
        col2.metric(label = 'Visibility (Kms)', value = round(self.visibility,1))
        col3.metric(label = "Maximum Temperature (Celsius)", value = round(self.max_temperature,1))
        col4.metric(label = "Wind", value = round(self.wind,1))


    def summary(self):
        #st.write("Current year month",self.current_year_month)
        current_month = self.today.split('-')[1]
        st.subheader("Summary for  " + self.lookup(current_month))
        req = self.df.loc[self.df.index.month == self.td.month]
        #st.dataframe(req)
        self.mean_for_month_usually = req.storage_tmc_pct.mean()
        usual = self.mean_for_month_usually

        if usual - self.today_metric > 0:
            compare_to_usual = "less"
        else:
            compare_to_usual = "more"
        """
        X= np.asarray(self.df1[['storage_tmc_pct','date']].loc[self.actual_mask_month].date)
        Y= np.asarray(self.df1[['storage_tmc_pct','date']].loc[self.actual_mask_month].storage_tmc_pct)
        X = sm.add_constant(X)
        model = sm.OLS(Y,X)
        results = model.fit()
        st.write("education", results.weights)
        """
        self.start_date = str(self.td - relativedelta(months=+3))
        self.end_date = str(self.td + relativedelta(months=+3))

        self.actual_mask_month = (self.df1['date'] >= self.start_date) & (self.df1['date'] <= self.today)
        self.pred_mask_month = (self.df1['date'] >= self.today) & (self.df1['date'] <= self.end_date)

        data = self.df1[['storage_tmc_pct','date']].loc[self.actual_mask_month]
        fig = px.scatter(data, x="date", y="storage_tmc_pct", trendline="ols")
        

        results = px.get_trendline_results(fig)
        #print(results)
        #st.plotly_chart(fig)
        past_2_months_type = results.iloc[0]["px_fit_results"].params[1]

        if past_2_months_type > 0:
            past_2_months_trend= "increasing"
        else:
            past_2_months_trend = "decreasing"

        #print(results)
        #st.plotly_chart(fig)
        next_2_months_trend = self.calc_trend('storage_tmc_pred_pct')


    
        temperature_type = self.calc_trend('precip')

        
        rainfall_type = self.calc_trend('precip')



        summary_point_1 = ["- PAST TREND : The water storage observed has been" , past_2_months_trend, "over past two months. "]
        extras1 = [ "start_month_storage", 'pct  in' , "start_month",  "to ", "current_month_storage", "pct in", "current month"]
        summary_point_2 = [ "- TEMPERATURE AND STORAGE FORECAST : With recent trend of" , temperature_type,"temperatures and", rainfall_type, "rainfall water level is expected to observe" , next_2_months_trend," trend for the next few months."]
        extras2 = ["next_2_months_storage", "in", "next_2_months_month"]
        summary_point_3 = ["- HISTORIC TRENDS FOR THE MONTH : The mean storage levels for this month are", compare_to_usual, "than the historic level of ", str(round(usual,1)) , '%']
        
        st.write(" ".join(summary_point_1))
        st.write(" ".join(summary_point_2))
        st.write(" ".join(summary_point_3))

    def risk_advisory(self):
        data_for_risk = self.df.loc[self.df.index == (self.td + timedelta(days=2))].storage_tmc_pred_pct.values[0]
        #st.write("data for risk", data_for_risk)
        if (data_for_risk > 90 ):
            self.advise = "Predicted storage levels critically high for next 2 days. Recommend precautionary measure to open gates"

        elif (data_for_risk < 25):
            self.advise = "Predicted storage levels critically low for next 2 days"

        else:
            self.advise = "There is no predicted risk/advisory. Outflow can follow standard procedure"
        
        
    
        
    def lookup(self,current_month):
        look_up = {'01': 'January', '02': 'February', '03': 'March', '04': 'April', '05': 'May',
            '06': 'June', '07': 'July', '08': 'August', '09': 'September', '10': 'October', '11': 'November', '12': 'December'}
        current_month_text = look_up[current_month]
       
        return current_month_text


    def calc_trend(self,param):
        data = self.df1[[param,'date']].loc[self.pred_mask_month]
        fig = px.scatter(data, x="date", y=param, trendline="ols")
        

        results = px.get_trendline_results(fig)
        #print(results)
        #st.plotly_chart(fig)
        param_type = results.iloc[0]["px_fit_results"].params[1]

        if param_type > 0:
            param_type_trend = "increasing"
        else:
            param_type_trend = "decreasing"

        return(param_type_trend)
