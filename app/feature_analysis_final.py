import pandas as pd
import streamlit as st 
import plotly.express as px
import os 
#import plotly.figure_factory as ff
from connection_setup import CONN
import plotly.graph_objects as go
from plotly.subplots import make_subplots
#from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from help import FeatureAnalysisHelp,FeatureAnanlysisTextualContent

class FeatureAnalysis():
    def __init__(self):
        self.TimeFactorSelection = " "
        self.LocationFactorSelection = " "
        self.df2 = pd.DataFrame()
        self.WeatherParamSelection = " "
        self.ft = FeatureAnanlysisTextualContent()
        self.fh = FeatureAnalysisHelp()
        self.krs = pd.read_sql("select storage_tmc,inflow_cusecs,outflow_cusecs from water where reservoir = 'krs'", con=CONN)

    def select_inputs(self):
        
        
        
        self.display_links()
        st.header("Overview")
        st.write(self.ft.FaWeatherParamText)
        self.df = self.krs
        index_names = self.df[self.df['inflow_cusecs'] == '&nbsp;' ].index
        self.df = self.df.drop(index_names)
        self.df.inflow_cusecs = pd.to_numeric(self.df.inflow_cusecs)
        #st.dataframe(self.df)
        self.corr = self.df.corr()
        #st.dataframe(self.corr)
        self.fig = px.imshow(self.corr)                 
        st.plotly_chart(self.fig)
        st.write(self.ft.FaDamParamHeatMapAnalysis)


        st.header("Inflow Dynamics",'inflow')
        st.write(self.ft.FaInflowDynamicsIntroText)

    
        self.fcol1, self.fcol2 = st.columns([1,3])
        self.df = pd.read_sql("SELECT * FROM weather where location == 'karnataka'", con=CONN)
        self.req = self.df.set_index(pd.to_datetime(self.df['date']))
        map_param = {'View All': ['max_temp','visibility','cloudcover','humidity'],'Maximum Temperature ': 'max_temp', 'Visibility': 'visibility','Cloud Cover': 'cloudcover','Humidity': 'humidity'}
        self.weather_selected = self.fcol1.selectbox("Please select the weather parameter for which you would like to view weather data ",
                     map_param.keys(),help = self.fh.FaSelectWeatherParameterDropdown)

        self.weather_param = map_param.get(self.weather_selected)

        if self.fcol1.checkbox('Display monthly plot for selected year',help = self.fh.FaSelectYearCheckBox):
            year = self.fcol1.slider("Year",2011,2020)
            input_date = str(year)
            if self.fcol1.checkbox('Display daily data for selected month',help = self.fh.FaSelectMonthCheckBox):

                month = self.fcol1.slider("Month",1,12)


                if month <10:
                    input_date = str(year) + '-' + '0' +  str(month)
                else:
                    input_date = str(year) + '-' + str(month)
            self.req = self.req.loc[input_date]

        #self.col1.write('Showing details for',self.weather_selected)

    def display_weather_graph(self):
        self.select_inputs()
        #.set_subplots(1, 4, horizontal_spacing=0.1)
        if self.weather_selected == 'View All':

            self.req = self.req[self.weather_param]
            fig = make_subplots(rows=4, cols=1, subplot_titles=self.req.columns)
            j = 1
            for i in self.req.columns:
                fig.add_trace(
                go.Scatter(
                    {'x': self.req.index, 
                    'y': self.req[i]},showlegend = False), 
                     row=j, col=1)
                j += 1
            self.fcol2.plotly_chart(fig)

        else:
            fig = go.Figure()

            fig.add_trace(go.Scatter(x = self.req.date,y = self.req[self.weather_param]))
            self.fcol2.plotly_chart(fig)

    def display_links(self):
        col1,col2 = st.columns(2)
        col1.write(" [Inflow Dynamics](#inflow)")
        col2.write(" [Outflow Dynamcis](#outflow)")

    def inflow_time(self):
        self.display_weather_graph()
        st.subheader("Time Factor")
        st.write(self.ft.FaTimeFactorText)
        st.slider("Select number of days cumulative", 1, 21)
        st.selectbox("Select type of data", ['type1','type2'])
        col1, col2= st.columns(2)
        hm1 = self.df[:-5]
        hm2 = self.df[:5]
        corr1 = hm1.corr()
        corr2 =hm2.corr()
        col1.plotly_chart(px.imshow(corr1))
        col2.plotly_chart(px.imshow(corr2))