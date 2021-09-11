import streamlit as st
import numpy as np
import pandas as pd


def display_toc():
    col1, col2, col3, col4 = st.columns(4)
    col1.write(" [Predictions](#predictions)")
    col3.write(" [Feature Analysis](#featureAnalysis)")
    
    
