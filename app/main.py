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
st.set_page_config(layout='wide', page_title = 'Arghyam')
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
    main_menu_list = ['Home','Historic data and Predictions','Exploring Weather and Dam data']
    main_menu_selection = st.sidebar.selectbox("Select Page", main_menu_list)
    
    if main_menu_selection == 'Home':
        st.header("KRS Dam Real-Time Water Level Prediction")
        Home()

    if main_menu_selection == 'Historic data and Predictions':
        st.title('Predictions','predictions')
        predictions = Predictions()
        predictions.display_forecast_plotly()
    if main_menu_selection == 'Exploring Weather and Dam data':
        fa = FeatureAnalysis()
        fa.execute()
    #st.write(" [Scroll to top](#t1)")

    # Add chatbot
    html_file = open(get_full_path("ChatbotWidget-main", "index.html") , 'r', encoding = 'utf-8').read()
    sthtml(html_file, height = 550, width = 370)


if __name__ == "__main__":
    main()
