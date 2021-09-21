### Predictions 
import pandas as pd
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
from help import PredictionsHelp
import plotly.graph_objects as go
from PIL import Image 
from setup import get_full_path
#import plotly.express as px

class Predictions:
    def __init__(self):
        #self.col1,self.col2 = st.columns(2)
        self.help = PredictionsHelp()
        self.actual = pd.read_sql("select date, storage_tmc from water where reservoir='krs'", con=CONN)
        self.pred = pd.read_sql("select date, model, storage_tmc from water_forecast",con = CONN)
        self.modeltitles = [x['title'] for x in MODELS]
        self.model_selected = st.sidebar.selectbox("Select model", self.modeltitles, help = self.help.predictionSelectModelDropdown)
        self.model = [item['number'] for item in MODELS if item['title'] == self.model_selected][0]
        self.validationLoss = [item['validation loss'] for item in MODELS if item['title'] == self.model_selected][0]
        self.df = pd.DataFrame()



    def input_model_and_date(self):
        self.pred = self.pred[self.pred['model']==self.model]
        self.find_last_n_days()


        self.actual['date'] = pd.to_datetime(self.actual['date'])
        self.pred['date'] = pd.to_datetime(self.pred['date'])
        self.pred['storage_tmc_prediction'] = self.pred['storage_tmc']
        self.pred.drop(columns = ['storage_tmc','model'],inplace=True)

        self.df = pd.merge(self.actual, self.pred, on = 'date', how = 'outer')
        self.df.set_index('date',inplace = True)
    
        self.df = self.weekly_plot()

        if st.sidebar.checkbox('Display monthly forecast plot for selected year',help = self.help.predictionSelectYearCheckBox):
                forecast_year = st.sidebar.slider("Select Year",2019,2021)
                input_date = str(forecast_year)
                if st.sidebar.checkbox('Check box to further zoom into selected month'):

                    forecast_month = st.sidebar.slider("Select Month",1,12)


                    if forecast_month <10:
                        input_date = str(forecast_year) + '-' + '0' +  str(forecast_month)
                    else:
                        input_date = str(forecast_year) + '-' + str(forecast_month)
                
                self.df = self.df.loc[input_date]
                

    def find_last_n_days(self):
        details = [item for item in MODELS if item['title'] == self.model_selected][0]
        last_n_days = details.get('HORIZON') 

        #if self.col1.checkbox("Display last " +  str(last_n_days) + " days prediction data"):
            #self.col1.dataframe(self.pred[-last_n_days:])


    def weekly_plot(self):
        plot_type_selected = st.sidebar.selectbox("Please select graph type", ['Average Weekly Forecast', 'Daily Forecast'],help = self.help.predictionSelectGraphType)
        if (plot_type_selected == 'Daily Forecast'):
            pass 
        if(plot_type_selected == 'Average Weekly Forecast'):
            self.df = self.df.resample('W-Mon').mean()
        return self.df

    def display_forecast_plotly(self):

        self.input_model_and_date()
        self.df = self.df.sort_values(by = 'date')
        self.df['dam_capacity'] = 49.45
        self.df['dead_storage'] = 4 
        self.df['graph_confidence'] = self.validationLoss**0.5*50
        self.df['limit_confidence'] = 2 
        #self.df['dam_capacity_lower'] = self.df['dam_capacity'] - self.df['limit_confidece']

        #self.df['dead_storage_upper'] = self.df['dead_storage'] + self.df['limit_confidece']


        fig = go.Figure()

        fig.add_trace(go.Scatter(x = self.df.reset_index().date,y = self.df['storage_tmc'],
        name='Actual Values',
        mode='lines',
        line=dict(color='firebrick')))

        fig.add_trace(go.Scatter(
        name='Prediction',
        x=self.df.reset_index().date,
        y=self.df['storage_tmc_prediction'],
        mode='lines',
        line=dict(color='royalblue')))

        fig.add_trace(go.Scatter(
        name='Prediction_Upper_Bound',
        x=self.df.reset_index().date,
        y=self.df['storage_tmc_prediction']+self.df['graph_confidence'],
        mode='lines',
        fillcolor='rgba(0,176,246,0.2)',
        fill='tonexty',
        showlegend = False,
        line=dict(color='rgba(0,176,246,0.2)')))

        fig.add_trace(go.Scatter(
        name='Prediction_Lower_Bound',
        x=self.df.reset_index().date,
        y=self.df['storage_tmc_prediction']-self.df['graph_confidence'],
        mode='lines',
        fillcolor='rgba(0,176,246,0.2)',
        fill='tonexty',
        showlegend = False,
        line=dict(color='rgba(0,176,246,0.2)')))

        fig.add_trace(go.Scatter(
        name='Dam at Full Capacity',
        x=self.df.reset_index().date,
        y=self.df['dam_capacity'],
        mode='lines',
        line=dict(color='black')))

        fig.add_trace(go.Scatter(
        name='Dam Capacity Limit',
        x=self.df.reset_index().date,
        y=self.df['dam_capacity'] - self.df['limit_confidence'],
        mode='lines',
        fillcolor='rgba(0,176,246,0.2)',
        fill='tonexty',
        showlegend = False,
        line=dict(color='rgba(0,176,246,0.2)')))

        fig.add_trace(go.Scatter(
        name='Dead Storage',
        x=self.df.reset_index().date,
        y=self.df['dead_storage'],
        mode='lines',
        line=dict(color='green')))

        fig.add_trace(go.Scatter(
        name='Dead Storage Limit',
        x=self.df.reset_index().date,
        y=self.df['dead_storage'] + self.df['limit_confidence'],
        mode='lines',
        fillcolor='rgba(0,176,246,0.2)',
        fill='tonexty',
        showlegend = False,
        line=dict(color='rgba(0,176,246,0.2)')))

        fig.update_layout(autosize=True,
        margin=dict(l=20, r=20, t=20, b=20),
        #paper_bgcolor="LightSteelBlue",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
        )
    

        summary_expander = st.expander("Expand to see training details")
        with summary_expander:

            model = [item for item in MODELS if item['title'] == self.model_selected][0]
            
            st.markdown(f"""
### MODEL: {model['title']}
* Training Window Size: {model["T"]}
* Prediction Window Size: {model["HORIZON"]}
* Training Features: {model["features"]}
* Model Summary: {model["model summary"]}
* Training Loss: {model["training loss"]}
* Validation Loss: {model["validation loss"]}
* **R2**- Coefficient of Determination: **{round(model["R2"], 2)}**
* **RMSE** - Root Mean Square Error: **{round(model["RMSE"], 2)}**
* Number of Paramaters: {model["parameters"]}
* LOSS Metric: MSE

### Train - Validation - Test split
            """)

            im3 = Image.open(get_full_path("Images", "tvtsplit.png"))
            st.image(im3, caption = 'Train/Validation/Test split for model training', width=600)

            st.markdown("### Model Architecture")
            im2 = Image.open(get_full_path("Images", "model.jpg"))
            st.image(im2, caption = 'LSTM Model Architecture', width=600)
    

        st.plotly_chart(fig, use_container_width=True)

        summary_expander2 = st.expander("Expand to see training details")
        with summary_expander2:
            st.markdown("### Level of Uncertainty")
            st.text("Uncertainty can be represented by a Gaussian with the below mentioned means and deviations for the various trained models. The best model is highlighted.")
            im3 = Image.open(get_full_path("Images", "confidence.jpg"))
            st.image(im3, caption = 'Uncertainty represented as standard deviations of error in TMC for various models', width=400)

            


        
        

        