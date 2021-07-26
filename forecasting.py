from tensorflow import keras 
from utils import TimeSeriesTensor
from sklearn.preprocessing import MinMaxScaler
from datetime import date, timedelta

from setup import get_full_path
import db
import pandas as pd

def predict(modelconfig, afterdate):
    T = modelconfig['T']
    LATENT_DIM = T
    HORIZON = modelconfig['HORIZON']

    # fetch data
    data = db.appdb.get_data_for_prediction(afterdate, T)

    # process data
    krs = pd.DataFrame(data, columns=['date', 'present_storage_tmc', 'inflow', 'outflow', 'max_temp', 'visibility', 'wind', 'humidity', 'cloudcover'])
    #krs = krs.drop_duplicates(subset=["date"])
    krs.date = pd.to_datetime(krs.date)
    krs['inflow'] = pd.to_numeric(krs.inflow, errors='coerce')
    krs['outflow'] = pd.to_numeric(krs.outflow, errors='coerce')
    krs['inflow_tmc'] = krs['inflow'] /11000
    krs['outflow_tmc'] = krs['outflow'] / 11000
    krs.sort_values(by=['date'], inplace=True, ascending=True)
    krs.set_index('date', inplace=True)
    krs = krs.sort_index(axis=1)

    # prepare tensor
    ts_data_load = krs[[ "present_storage_tmc", "inflow_tmc", "outflow_tmc", "max_temp", "visibility", "humidity", "wind"]]
    ts_data_load.sort_index(axis = 1)
    X_scaler = MinMaxScaler()
    tensor = X_scaler.fit_transform(ts_data_load)
    tensor = tensor.reshape((1, *(tensor.shape)))
    print(tensor.shape)


    # fetch model
    model_path = f'./models/{modelconfig["folder"]}' #get_full_path("models", modelconfig["folder"])
    print("LOADING...", model_path)
   
    model = keras.models.load_model(model_path)
    print(model.summary())
    # run predictions
    y_scaler = MinMaxScaler()
    y_scaler.fit(krs[["present_storage_tmc"]])
    ts_predictions = model.predict(tensor)
    ts_predictions = y_scaler.inverse_transform(ts_predictions)[0]
    print(ts_predictions)
    # store this in db
    # for t in range(1, HORIZON+1):
    #     dt = afterdate + timedelta(t)
    #     db.appdb.upsert_forecast_record((str(dt), modelconfig["reservoir"], ts_predictions[t-1], modelconfig["number"]))
    
    # db.appdb.commit()