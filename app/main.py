import pandas as pd
from pathlib import Path
#import sqlite3
#from sqlite3 import Connection

from pandas.core.frame import DataFrame
import streamlit as st
import matplotlib.pyplot as plt
import datetime 
from sklearn.preprocessing import MinMaxScaler
import seaborn as sns
from setup import MODELS
import toc
from home import Home
from predictions import Predictions
from feature_analysis_final import FeatureAnalysis


#st.set_page_config(layout='wide')

def main():
    
    
    main_menu_list = ['Home','Historic data and Predictions','How was the data calculated?']
    main_menu_selection = st.sidebar.selectbox("Select Page", main_menu_list)
    if main_menu_selection == 'Home':
        st.title("Team Arghyam",'t1')
        st.header("KRS Water level prediction")
        Home()

    if main_menu_selection == 'Historic data and Predictions':
        st.title('Predictions','predictions')
        predictions = Predictions()
        predictions.display_forecast_plotly()
    if main_menu_selection == 'Feature Analysis':
        st.title('Feature Analysis', 'featureAnalysis')
        fa = FeatureAnalysis()
        fa.inflow_time()
    #st.write(" [Scroll to top](#t1)")


if __name__ == "__main__":
    main()
