import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import seaborn as sns
import streamlit as st
from sklearn.preprocessing import MinMaxScaler

# load krs dam file 
krs = pd.read_csv("KRS.csv")

# load mysore weather data 
wtr = pd.read_csv("krishnarajanagara.csv")
st.title("Correlation between KRS dam and weather data")

# create datetime objects for both the files
krs['Date'] = pd.to_datetime(krs['FLOW_DATE'])
wtr['Date'] = pd.to_datetime(wtr['Date time'])

#merging 2 files such that dates common for both files are included in one dataset
res = krs.merge(wtr)

cols = ['Wind Chill','Snow','Snow Depth','Wind Gust','Conditions','Name','RESERVOIR','UNIQUE_KEY','FLOW_DATE',]
res.drop(columns = cols, inplace = True)

cols = ['Date time', 'Date']
req = res.drop(columns = cols)

# normalising data

mms = MinMaxScaler()
df = pd.DataFrame(mms.fit_transform(req),columns = req.columns)
st.write('Data after conversion to min max scale')
st.write(df.head())
# Display full data base on checkbox.
if st.checkbox('show full data'):
    df
st.write("HeatMap for correlation between various features of data collected")
#heatmap for normalised data
cor = df.corr()
fig, ax = plt.subplots(figsize=(10,10)) 
sns.heatmap(cor, xticklabels=cor.columns, yticklabels=cor.columns, annot=True,ax = ax)
st.pyplot(fig)
