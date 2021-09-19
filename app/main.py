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
from streamlit.components.v1 import html as sthtml

import sys
import os
  
# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))
  
# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)
  
# adding the parent directory to 
# the sys.path.
sys.path.append(parent)
# https://python.plainenglish.io/three-tips-to-improve-your-streamlit-app-a4c94b4d2b30
from setup import MODELS, get_full_path
import toc
from home import Home
from predictions import Predictions
from feature_analysis_final import FeatureAnalysis
from PIL import Image

#st.set_page_config(layout='wide')
def main():
    st.markdown(""" 
<style> 
    .css-hi6a2p {max-width: 100%; padding: 3rem;}
    .main iframe {position: fixed; bottom: 10px; right:10px; z-index:100000;}
</style>
""", unsafe_allow_html=True)

    logoFile = Image.open(get_full_path("Images", "logo.png"))
    st.sidebar.image(logoFile)
    main_menu_list = ['Home','Historic data and Predictions','Feature Analysis']
    main_menu_selection = st.sidebar.selectbox("Select Page", main_menu_list)
    
    if main_menu_selection == 'Home':
        st.header("KRS Dam Real-Time Water Level Prediction")
        Home()

        st.markdown("""
        ### KRS Dam's connection to Bangalore
        **Bangalore**, located in the southeastern part of Karnataka, is the sixth largest city of India and one of the fastest growing
        cities of Asia, with a total population of close to 10 million. *Encroachment* and *unplanned urbanization* over the past 4 decades 
        has cost the city heavily in terms of its water bodies. Today the number of water bodies in the city is just over 20% of 
        what once existed. Bengaluru has two main sources of water:  The River Kaveri (Cauvery) and Groundwater. 
        Water from the Cauvery is collected in the Krishna Raja Sagar Dam in Mysore. From here, the BWSSB (Bangalore Water Supply
         and Sewerage Board) pumps water and transports it to over 660,355 BWSSB 
         connections in Bengaluru
        """)

    if main_menu_selection == 'Historic data and Predictions':
        st.title('Predictions','predictions')
        predictions = Predictions()
        predictions.display_forecast_plotly()
    if main_menu_selection == 'Feature Analysis':
        fa = FeatureAnalysis()
        fa.execute()
    #st.write(" [Scroll to top](#t1)")

    # Add chatbot
    html_file = open(get_full_path("ChatbotWidget-main", "index.html") , 'r', encoding = 'utf-8').read()
    sthtml(html_file, height = 550, width = 370)


if __name__ == "__main__":
    main()
