from tensorflow import keras 
from utils import TimeSeriesTensor
from sklearn.preprocessing import MinMaxScaler

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

from config.files import get_full_path
import db
import pandas as pd

data = db.appdb.get_data_for_prediction(30) # data for last 30 days from today
print(data)
krs = pd.DataFrame(data, columns=['date', 'present_storage_tmc', 'inflow', 'outflow', 'max_temp', 'visibility', 'wind', 'humidity', 'cloudcover'])
krs = krs.drop_duplicates(subset=["date"])
krs.date = pd.to_datetime(krs.date)
krs['inflow'] = pd.to_numeric(krs.inflow, errors='coerce')
krs['outflow'] = pd.to_numeric(krs.outflow, errors='coerce')
krs['inflow_tmc'] = krs['inflow'] /11000
krs['outflow_tmc'] = krs['outflow'] / 11000
krs.sort_values(by=['date'], inplace=True, ascending=True)
krs.set_index('date', inplace=True)
krs = krs.sort_index(axis=1)
print(krs.info())

T = 30
LATENT_DIM = T
HORIZON = 1


ts_data_load = krs[[ "present_storage_tmc", "inflow_tmc", "outflow_tmc", "max_temp", "visibility", "humidity", "wind"]]
ts_data_load.sort_index(axis = 1)
features = len(ts_data_load.columns)
flist = list(ts_data_load.columns)
tensor_structure = {"X": (range(-T + 1, 1), flist)}



checkpoint_path = get_full_path("forecasting", "models", "30dayto1day")
print("checkpoint path = ", checkpoint_path)

model = keras.models.load_model(checkpoint_path)

X_scaler = MinMaxScaler()
y_scaler = MinMaxScaler()
y_scaler.fit(krs[["present_storage_tmc"]])
ts_data_load[flist] = X_scaler.fit_transform(ts_data_load)
ts_data_inputs = TimeSeriesTensor(ts_data_load, "present_storage_tmc", HORIZON, tensor_structure, freq='D')
ts_predictions = model.predict(ts_data_inputs["X"])
ts_predictions = y_scaler.inverse_transform(ts_predictions)

print(ts_predictions)
# store this in db for tommorrow

