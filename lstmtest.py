import datetime as dt
import os
import warnings
from collections import UserDict
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from utils import TimeSeriesTensor, mape, extract_data, create_evaluation_df
import db
from sklearn.preprocessing import MinMaxScaler
from tensorflow import keras

# fetch data
data = db.appdb.get_data_for_training()

# process data
krs = pd.DataFrame(data, columns=['date', 'present_storage_tmc', 'inflow', 'outflow', 'max_temp', 'visibility', 'wind', 'humidity', 'cloudcover'])
#krs = krs.drop_duplicates(subset=["date"])
krs = krs.drop_duplicates(subset=["date"])
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
flist = list(ts_data_load.columns)
features = len(ts_data_load.columns)

valid_st_data_load = "2018-01-01 00:00:00"
test_st_data_load = "2020-01-01 00:00:00"

#valid_st_data_load = "2020-01-01 00:00:00"
#test_st_data_load = "2020-01-01 00:00:00"

T = 180
HORIZON = 90
#X_scaler = MinMaxScaler()
train = ts_data_load.copy()[ts_data_load.index < valid_st_data_load]

#y_scaler = MinMaxScaler()
#y_scaler.fit(train[["present_storage_tmc"]])

#train[flist] = X_scaler.fit_transform(train)
train = train.dropna(axis = 0, how ='any')
print(train.shape)


tensor_structure = {"X": (range(-T + 1, 1), flist)}
print(tensor_structure)
ts_train_inp = TimeSeriesTensor(
    dataset=train,
    target="present_storage_tmc",
    H=HORIZON,
    tensor_structure=tensor_structure,
    freq="D",
    drop_incomplete=True,
)
back_ts_data = dt.datetime.strptime(valid_st_data_load, "%Y-%m-%d %H:%M:%S") - dt.timedelta(days=T - 1)
valid = ts_data_load.copy()[(ts_data_load.index >= back_ts_data) & (ts_data_load.index < test_st_data_load)]
#valid[flist] = X_scaler.transform(valid)
valid_inputs = TimeSeriesTensor(valid, "present_storage_tmc", HORIZON, tensor_structure, freq='D')


from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.layers import GRU, Dense, LSTM
from tensorflow.keras.models import Model, Sequential

LATENT_DIM = 100#(T+HORIZON)//2
BATCH_SIZE = 16
EPOCHS = (
    100
)
DROPOUT = 0.1
RECURRENT_DROPOUT=0.2

checkpoint_filepath = "./models/180daysto90day"
if not os.path.exists(checkpoint_filepath):
    os.makedirs(checkpoint_filepath)
    print("saving model")
    model = Sequential()
    model.add(LSTM(LATENT_DIM, recurrent_dropout=DROPOUT, dropout=DROPOUT, input_shape=(T, features)))
    #model.add(GRU(LATENT_DIM, input_shape=(T, 3)))
    #model.add(LSTM(LATENT_DIM, recurrent_dropout=RECURRENT_DROPOUT, dropout=DROPOUT))
    model.add(Dense(HORIZON))
    model.compile(optimizer="adam", loss="mse")
    model.save(checkpoint_filepath)
else:
    print("loading saved model")
    model = keras.models.load_model(checkpoint_filepath)
    #model.load_weights(checkpoint_filepath)

model.summary()

earlystop = EarlyStopping(monitor="val_loss", min_delta=0, patience=20, verbose=1)
model_checkpoint_callback = ModelCheckpoint(
    filepath=checkpoint_filepath,
    save_weights_only=False,
    monitor='val_loss',
    mode='min',
    verbose=1,
    save_best_only=True)

model_history = model.fit(
    ts_train_inp["X"],
    ts_train_inp["target"],
    batch_size=BATCH_SIZE,
    epochs=EPOCHS,
    validation_data=(valid_inputs["X"], valid_inputs["target"]),
    callbacks=[model_checkpoint_callback], #, earlystop],
    verbose=1,
)

# load the best model
model = keras.models.load_model(checkpoint_filepath)
back_ts_data = dt.datetime.strptime(test_st_data_load, "%Y-%m-%d %H:%M:%S") - dt.timedelta(
    days=T - 1
)
ts_data_test = ts_data_load.copy()[test_st_data_load:]
print(ts_data_test.shape)
#ts_data_test[flist] = X_scaler.transform(ts_data_test)
ts_data_test_inputs = TimeSeriesTensor(ts_data_test, "present_storage_tmc", HORIZON, tensor_structure, freq='D')

def create_evaluation_df1(predictions, test_inputs, H):#, scaler):
    """Create a data frame for easy evaluation"""
    eval_df = pd.DataFrame(
        predictions, columns=["t+" + str(t) for t in range(1, H + 1)]
    )
    
    eval_df["timestamp"] = test_inputs.dataframe.index
    print(eval_df.shape, eval_df.head(2))

    #eval_df = pd.melt(
    #    eval_df, id_vars="timestamp", value_name="prediction", var_name="h"
    #)
    values = ['t+'+str(i) for i in range(1, H+1)]
    
    eval_df = pd.melt(
        eval_df, id_vars="timestamp", value_vars=values, value_name="prediction"
    )
    print(eval_df.shape, eval_df.head(2))
    eval_df["actual"] = np.transpose(test_inputs["target"]).ravel()
    #eval_df[["prediction", "actual"]] = scaler.inverse_transform(
    #    eval_df[["prediction", "actual"]]
    #)
    return eval_df

ts_predictions = model.predict(valid_inputs["X"])
ev_ts_data = create_evaluation_df1(ts_predictions, valid_inputs, HORIZON)#, y_scaler)
print(ev_ts_data)

print(mape(ev_ts_data["prediction"], ev_ts_data["actual"]))

print(ts_predictions[0], valid_inputs['X'][0])
