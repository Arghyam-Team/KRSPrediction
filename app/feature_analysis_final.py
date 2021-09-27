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
from PIL import Image 
from setup import get_full_path

class FeatureAnalysis():

    def get_dam_data(self, dam):
        df = pd.read_sql(f"select storage_tmc,inflow_cusecs,outflow_cusecs,date from water where reservoir = '{dam}' order by realdate", con=CONN)
        index_names = df[(df['inflow_cusecs'] == '&nbsp;') | (df['outflow_cusecs'] == '&nbsp;') | (df['storage_tmc'] == '&nbsp;')].index

        df = df.drop(index_names)
        df.inflow_cusecs = pd.to_numeric(df.inflow_cusecs, errors='coerce')
        df.outflow_cusecs = pd.to_numeric(df.outflow_cusecs, errors='coerce')
        df.storage_tmc = pd.to_numeric(df.storage_tmc, errors='coerce')

        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
        df.set_index(df['date'], inplace=True)
        df = df.sort_index(axis=0)
        df = df.drop(columns=['date'])

        return df
    def __init__(self):
        self.krs = self.get_dam_data('krs')


        self.weather = pd.read_sql("SELECT max_temp, wind, visibility, cloudcover, humidity, precip, date FROM weather where location == 'karnataka' order by realdate", con=CONN)
        self.weather['date'] = pd.to_datetime(self.weather['date'], format='%Y-%m-%d')
        self.weather.set_index(self.weather['date'], inplace=True)
        self.weather = self.weather.sort_index(axis=0)
        self.weather = self.weather.drop(columns=['date'])


    def execute(self):
        select = st.sidebar.selectbox('Related Data', ['KRS Dam data', 'Karnataka Weather', 'KRS vs Kabini, Harangi, Hemavathi'], key=1)
    
        if select == 'KRS Dam data':
            self.show_dam_data()
        elif select == 'Karnataka Weather':
            self.show_weather()
        else:
            self.show_multi_dams()

    def process(self, df, prefix):
        import re
        df.columns = [prefix+re.sub(r'_(.*)', '', x) for x in df.columns]
        return df

    def show_multi_dams(self):
        hemavathi = self.process(self.get_dam_data('hemavathi'), "hemavathi_")
        kabini = self.process(self.get_dam_data('kabini'), "kabini_")
        harangi = self.process(self.get_dam_data('harangi'), "harangi_")
        krs = self.process(self.get_dam_data('krs'), "krs_")

        df = krs.join(hemavathi.join(kabini.join(harangi)))

        show_yearly = False
        year = 0
        st.title('KRS Vs Hemavathi, Kabini & Harangi')
        st.markdown("""There is significat correlation between the upstream dams and the KRS dam, therefore to keep the model simple,
        using krs features should be sufficient.
        """)

        # summary_expander = st.expander("Expand to see relevant data")
        # with summary_expander:
        #     image_file = Image.open(get_full_path("Images", "landuse.jpg"))
        #     st.image(image_file,caption = 'Land use dynamics in the greater Bangalore region',width = 600)

        #     image_file = Image.open(get_full_path("Images", "recommended.jpg"))
        #     st.image(image_file,caption = 'Monthly KRS Dam recommended water releases to the irrigation and drinking water supply',width = 600)
        #     st.markdown("[source](http://waterresources.kar.nic.in/KRS_OM_KaWRD.pdf)")
        
        if st.sidebar.checkbox('Display yearly data'):
            show_yearly = True
            year = st.sidebar.slider("Select Year",2011,2021)
            df = df.loc[(df.index >= f'{year}-01-01') & (df.index <= f'{year}-12-31') ]

        corr = df.corr()
        fig = px.imshow(corr, color_continuous_scale=px.colors.sequential.Cividis_r)
        st.markdown("### Correlation between different Dam features")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("* Realtime dam data source: [IMS](http://122.15.179.102/ARS/home/reservoir)")

        

    def show_weather(self):
       
        show_yearly = False
        year = 0

        st.title('Karnataka Weather Data')
        st.markdown("""
        As the map below shows, the topology of the KRS dam will benefit from rains in several cities like 
        Haranhalli, Heggadikpplu, Akkihebbal, Chikmanglur, Keralapura, Kodugu, Krishnarajanagara, Mandya, Mysore and Saligrama. 
        All these regions are topographically at a higher elevation. Bangalore and further east regions are at lower topography. 
        While Bangalore rains may reduce outflow from KRS it has no impact on the inflow. 
        
        Analysis shows that each location had some correlation with the reservoi, however the average Karnataka 
        weather had more of a relationship. The relationships bolster as we look at **cumulative** weather. 
        """)

        summary_expander = st.expander("Expand to see relevant data")
        with summary_expander:
            im1 = Image.open(get_full_path("Images", "cloud_inflow.png"))
            im2 = Image.open(get_full_path("Images", "wind_inflow.png"))
            st.image([im1, im2],caption = ['Correlation between cumulative cloud cover and inflow', 'Correlation between cumulative wind and inflow'], width=400)
            st.text("* X-axis is number of days and y-axis is the correlation")
            st.markdown("Our **model choice of LSTM** was a reflection of this fact since LSTM can decide on forgetting and remembering relevant features and even chose to cumulate them as needed.")

            ima1 = Image.open(get_full_path("Images", "map.jpg"))
            st.image(ima1, caption="Cauvery Basin", width=400)

            ima2 = Image.open(get_full_path("Images", "map2.jpg"))
            st.image(ima2, caption="Locations considered during analysis")
            
            im3 = Image.open(get_full_path("Images", "cityvskarnataka.png"))
            st.image(im3, caption = 'correlation between overall karnataka and various cities weather with KRS dam features', use_column_width  = True)
            st.text("""* Notice how overall karnataka weather nicely summarizes the tred of various cities. There are some deviations in direction of correlation wthat may be related to specific topography, yet to be clearly explained.""")

            im4 = Image.open(get_full_path("Images", "weather_correlations.jpg"))
            
            st.image(im4, caption = 'Trend of overall karnataka weather and various KRS dam features', use_column_width  = True)
            st.text("* Notice how lower temperatures, and higher humidity or cloud cover is related to more storage")
        
        days = st.sidebar.slider("#Days Cumulative Weather",1, 60)
        
        if days > 1:
            sdf = self.weather.rolling(days).mean()
            df = sdf.join(self.krs)
        else:
            df = self.weather.join(self.krs)

        
        if st.sidebar.checkbox('Display yearly data'):
            show_yearly = True
            year = st.sidebar.slider("Select Year",2011,2021)
            df = df.loc[(df.index >= f'{year}-01-01') & (df.index <= f'{year}-12-31') ]
        
        corr = df.corr()
        fig = px.imshow(corr, color_continuous_scale=px.colors.sequential.Cividis_r)
        st.markdown("### Correlation between various Weather metrics")
        st.plotly_chart(fig, use_container_width=True)

        select_weather = st.sidebar.multiselect('Weather Features', ['All Weather Parameters', 'Maximum Temperature', 'Wind', 'Visibility', 'Cloud Cover', 'Humidity', 'Precipitation'], key=2, default = 'All Weather Parameters')
        select_dam = st.sidebar.multiselect('KRS Dam Features', ['All Dam Parameters', 'Inflow', 'Outflow', 'Storage'], key=3,default = 'Storage')
        m1 = {
            'Maximum Temperature': ['max_temp', 'firebrick'], 
            'Wind': ['wind', 'green'], 
            'Visibility': ['visibility', 'brown'], 
            'Cloud Cover': ['cloudcover', 'blue'], 
            'Humidity': ['humidity', 'lightblue'], 
            'Precipitation': ['precip', 'darkgreen']}
        m2 = {
            'Inflow': ['inflow_cusecs', 'green'], 
            'Outflow': ['outflow_cusecs', 'firebrick'], 
            'Storage': ['storage_tmc', 'darkblue']
            }
        if st.sidebar.checkbox("Compare weather and dam data in same plot"):
            st.markdown("#### Dam and Weather Parameter display")
            select = select_weather + select_dam
            m = m1.update(m2) #m1 | m2
            fig = go.Figure()
            if (len(select) != 0):
                fig = make_subplots(rows = len(select))
            else:
                fig = make_subplots(rows = 1)
            
            for i,param in enumerate(select):
                for key in m:
                    if param=='All Weather Parameters' or param=='All Dam Parameters' or param == key:
                        fig.add_trace(go.Scatter(x = df.index,y = df[m[key][0]],
                        name=key,
                        mode='lines',
                        line=dict(color=m[key][1])),row = i+1,col = 1)

            st.plotly_chart(fig, use_container_width=True)
            fig.update_layout(autosize=True,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="LightSteelBlue",
        yaxis_title="Storage in Percentage",
        xaxis_title="Date",
        )

        else:
          
            st.markdown("#### Weather Parameter display")
            fig = go.Figure()
            if (len(select_weather) != 0):
                fig = make_subplots(rows = len(select_weather))
            else:
                fig = make_subplots(rows = 1)
            
            for i,param in enumerate(select_weather):
                for key in m1:
                    if param=='All Weather Parameters'  or param == key:
                        fig.add_trace(go.Scatter(x = df.index,y = df[m1[key][0]],
                            name=key,
                            mode='lines',
                            line=dict(color=m1[key][1])),row = i+1,col = 1)

            st.plotly_chart(fig, use_container_width=True)


      

        
            st.markdown("#### Dam Parameter display")
            fig = go.Figure()
            if (len(select_dam) != 0):
                fig = make_subplots(rows = len(select_dam))
            else:
                fig = make_subplots(rows = 1)
            for i,param in enumerate(select_dam):
                for key in m2:
                    if  param=='All Dam Parameters' or param == key:
                        fig.add_trace(go.Scatter(x = df.index,y = df[m2[key][0]],
                        name=key,
                        mode='lines',
                        line=dict(color=m2[key][1])),row = i+1,col = 1)

  
        
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("* Weather data source: [Visual Crossing](https://www.visualcrossing.com/weather-data)")
        st.markdown("* Realtime dam data source: [IMS](http://122.15.179.102/ARS/home/reservoir)")

        

    
    def show_dam_data(self):
        df = self.krs

        show_yearly = False
        year = 0
        st.title('KRS Dam Data')
        st.markdown("""
Landusage over past decades have shown a major shift from agrarian to urban and industrial. 
The waterbodies have also shrunken over time. With the overall water use across consumers remaining stationary there are
only seasonal variations. The recommended release cycle have also remained the same. 
There is also a strong correlation between inflow and outflow, which also correlates to the overall Karnataka weather. 

*Since we are not studying groundwater, soil information and evapo-transpiration etc. are ruled out from this analysis.*
        """)

        summary_expander = st.expander("Expand to see relevant data")
        with summary_expander:
            image_file = Image.open(get_full_path("Images", "landuse.jpg"))
            st.image(image_file,caption = 'Land use dynamics in the greater Bangalore region',width = 600)

            image_file = Image.open(get_full_path("Images", "recommended.jpg"))
            st.image(image_file,caption = 'Monthly KRS Dam recommended water releases to the irrigation and drinking water supply',width = 600)
            st.markdown("[source](http://waterresources.kar.nic.in/KRS_OM_KaWRD.pdf)")

            im3 = Image.open(get_full_path("Images", "rec_outflow_dam.png"))
            st.image(im3, caption = 'Actual Vs Recommended Outflow. Notice the similarity in patterns', width=600)
            st.text("*The excess outflow is during the rainy seasons to keep the safe storage limits")
        
        if st.sidebar.checkbox('Display yearly data'):
            show_yearly = True
            year = st.sidebar.slider("Select Year",2011,2021)
            df = df.loc[(df.index >= f'{year}-01-01') & (df.index <= f'{year}-12-31') ]

        corr = df.corr()
        fig = px.imshow(corr)
        st.markdown("### Correlation between various Dam metrics")
        st.plotly_chart(fig, use_container_width=True)

        fig = go.Figure()

        fig.add_trace(go.Scatter(x = df.index,y = df['storage_tmc'],
        name='Storage(TMC)',
        mode='lines',
        line=dict(color='blue')))

        st.markdown("### Storage in TMC over the last decade")
        st.plotly_chart(fig, use_container_width=True)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x = df.index,y = df['inflow_cusecs']/327.74128,
        name='Inflow(TMC)',
        mode='lines',
        line=dict(color='green')))

        st.markdown("### Inflow in TMC over the last decade")
        if not show_yearly or (show_yearly and (year==2018 or year==2019)):
            st.write("Notice the peaks in 2018/19 indicating very high values due to flooding.")
        st.plotly_chart(fig, use_container_width=True)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x = df.index,y = df['outflow_cusecs']/327.74128,
        name='Outflow(TMC)',
        mode='lines',
        line=dict(color='firebrick')))

        st.markdown("### Outflow in TMC over the last decade")
        if not show_yearly or (show_yearly and (year==2018 or year==2019)):
          st.write("Notice the peaks in 2018/19 indicating very high values due to flooding.")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("* Realtime dam data source: [IMS](http://122.15.179.102/ARS/home/reservoir)")

    def select_inputs(self):
        
        self.display_links()
        st.header("Overview")
        st.write(self.ft.FaWeatherParamText)
        self.df = self.krs
        self.df.set_index('date')
        self.df.index = pd.to_datetime(self.df.index)
        self.df.sort_index(axis=0)

        index_names = self.df[self.df['inflow_cusecs'] == '&nbsp;' ].index

        self.df = self.df.drop(index_names)
        self.df.inflow_cusecs = pd.to_numeric(self.df.inflow_cusecs)
        #st.dataframe(self.df)
        self.corr = self.df.corr()
        #st.dataframe(self.corr)
        self.fig = px.imshow(self.corr)   
              
        st.plotly_chart(self.fig)
        st.write(self.ft.FaDamParamHeatMapAnalysis)

        # f = px.line(self.df, y="outflow_cusecs", x="date", title="Outflow data")     
        


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
