## KRS Dam Water Storage prediction

This repository contains the work done in developing a predictive model that estimates the reservoir water availability at least 1-3 months in advance using hydro-meteorological parameters and reservoir water level data for Wave2Web Hackathon. The main aim of this Hackathon is to develop a predictive model to forecast water availability in the select reservoir(s) supplying water in Bengaluru, India.

We have collected weather data, land use, water use to come up with a model based on historical water availability, hydro-meteorological data, and water demand. [This document](https://github.com/Arghyam-Team/KRSPrediction/blob/main/Arghyam%20Final%20Report.pdf) contains the complete details. 

We have trained several types of models using LSTM to forecast water availability for one day, 30 days, 60 days, and 90 days. The features considered for model training are Present storage in TMC, inflow, outflow, Maximum Temprature, visibility, humidity and wind. The details of the trained models are presented in the below table. 

<img src="https://github.com/Arghyam-Team/KRSPrediction/blob/main/Images/model%20summary.PNG" width="600" height="400">

The [prediction dashboard](http://65.2.75.233:8501/) is deployed in a free tier AWS EC2 instance using the python Streamlit library.

### Conclusion
- Proposed water availability prediction model for 1 - 3 months (30 days to 90 days) using deep learning from weather and reservior data.
- Complex models introduced overfitting as training data is limited. Simpler models resulted good accuracy.
- Weather data alone is also sufficient to predict the water availability.

### References
- [Sources of Drinking water in Bangalore](https://www.karnataka.com/bangalore/what-is-the-source-of-drinking-water-in-bangalore/)
- [Operation and Maintenance Manual for Krishnarajasagara Dam](http://waterresources.kar.nic.in/KRS_OM_KaWRD.pdf)

