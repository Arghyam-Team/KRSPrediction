from os.path import dirname, join

ROOT_DIR = dirname(__file__)

def get_full_path(*path):
    return join(ROOT_DIR, *path)

MODELS = [
    {'number': 14, 'title': '30 day Prediction from 30 day Window (Vanilla LSTM)', 'folder':'30daysto30daylstm', 'T':30, 'HORIZON': 30, 'reservoir': 'krs', 'features': 'Storage TMC, Inflow, Outflow, Max Temperature, Visibility, Wind, Humidity', 'model summary': 'Input -> LSTM (30 hidden units) -> Dense(30 outputs)','training loss' : 0.098 , 'validation loss': 0.0011, 'parameters':5490 },
    {'number': 13, 'title': '60 day Prediction from 60 day Window (Vanilla LSTM)', 'folder':'60daysto60daylstm', 'T':60, 'HORIZON': 60, 'reservoir': 'krs','features': 'Storage TMC, Inflow, Outflow, Max Temperature, Visibility, Wind, Humidity', 'model summary': 'Input -> LSTM (60 hidden units) -> Dense(60 outputs)','training loss' : 0.037 , 'validation loss': 0.0010, 'parameters':19980},
    {'number': 12, 'title': '90 day Prediction from 90 day Window (Vanilla LSTM)', 'folder':'90daysto90daylstm', 'T':90, 'HORIZON': 90, 'reservoir': 'krs', 'features': 'Storage TMC, Inflow, Outflow, Max Temperature, Visibility, Wind, Humidity', 'model summary': 'Input -> LSTM (90 hidden units) -> Dense(90 outputs)','training loss' : 0.098 , 'validation loss': 0.0011, 'parameters':43470},
    {'number': 9, 'title': '30 day Prediction from 180 day Window (Vanilla LSTM)', 'folder':'180daysto30dayo', 'T':180, 'HORIZON': 30, 'reservoir': 'krs', 'features': 'Storage TMC, Inflow, Outflow, Max Temperature, Visibility, Wind, Humidity', 'model summary': 'Input -> LSTM (40 hidden units) -> Dense(30 outputs)','training loss' : 0.0028 , 'validation loss': 0.0015, 'parameters':8910},
    {'number': 11, 'title': '60 day Prediction from 180 day Window (Vanilla LSTM)', 'folder':'180daysto60day', 'T':180, 'HORIZON': 60, 'reservoir': 'krs', 'features': 'Storage TMC, Inflow, Outflow, Max Temperature, Visibility, Wind, Humidity', 'model summary': 'Input -> LSTM (70 hidden units) -> Dense(60 outputs)','training loss' : 0.0048 , 'validation loss': 0.0015, 'parameters':26100},
    {'number': 10, 'title': '90 day Prediction from 180 day Window (Vanilla LSTM)', 'folder':'180daysto90day', 'T':180, 'HORIZON': 90, 'reservoir': 'krs', 'features': 'Storage TMC, Inflow, Outflow, Max Temperature, Visibility, Wind, Humidity', 'model summary': 'Input -> LSTM (100 hidden units) -> Dense(90 outputs)','training loss' : 0.059 , 'validation loss': 0.0016, 'parameters':52290},
    {'number': 8, 'title': '90 day Prediction from 30 day Weather forecast', 'folder':'30daysto1dayw', 'T':30, 'HORIZON': 1, 'reservoir': 'krs', 'onlyweather':True, 'features': 'Storage TMC, Max Temperature, Visibility, Wind, Humidity', 'model summary': 'Input -> LSTM (30 hidden units) -> Dense(1)','training loss' : 0.0008 , 'validation loss': 0.00038, 'parameters':4351}
    #{'number': 1, 'title': 'One day Prediction from 30 day Window', 'folder':'30daysto1day', 'T':30, 'HORIZON': 1, 'reservoir': 'krs'},
    #{'number': 2, 'title': '15 day Prediction from 30 day Window', 'folder':'30daysto15days', 'T':30, 'HORIZON': 15, 'reservoir': 'krs'},
    #{'number': 3, 'title': '30 day Prediction from 30 day Window', 'folder':'30daysto30days', 'T':30, 'HORIZON': 30, 'reservoir': 'krs','model type': 'LSTM - Deep Learning Model','training loss' : 0.0049 , 'validation loss': 0.0084},
    #{'number': 4, 'title': '30 day Prediction from 60 day Window', 'folder':'60daysto30days', 'T':60, 'HORIZON': 30, 'reservoir': 'krs'},
    #{'number': 5, 'title': '30 day Prediction from 90 day Window', 'folder':'90daysto30days', 'T':90, 'HORIZON': 30, 'reservoir': 'krs'},
    #{'number': 6, 'title': '60 day Prediction from 60 day Window', 'folder':'60daysto60days', 'T':60, 'HORIZON': 60, 'reservoir': 'krs'},
    #{'number': 7, 'title': '90 day Prediction from 90 day Window', 'folder':'90daysto90days', 'T':90, 'HORIZON': 90, 'reservoir': 'krs'},
    
]



