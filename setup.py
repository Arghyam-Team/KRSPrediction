from os.path import dirname, join

ROOT_DIR = dirname(__file__)

def get_full_path(*path):
    return join(ROOT_DIR, *path)

MODELS = [
    # {'number': 9, 'title': '30 day Prediction from 180 day Window (Vanilla LSTM)', 'folder':'180daysto30dayo', 'T':180, 'HORIZON': 30, 'reservoir': 'krs', 'model type': 'LSTM - Single layer','training loss' : 0.0028 , 'validation loss': 0.0015},
    {'number': 10, 'title': '90 day Prediction from 180 day Window (Vanilla LSTM)', 'folder':'180daysto90day', 'T':180, 'HORIZON': 90, 'reservoir': 'krs'}
    # {'number': 1, 'title': 'One day Prediction from 30 day Window', 'folder':'30daysto1day', 'T':30, 'HORIZON': 1, 'reservoir': 'krs'},
    # {'number': 2, 'title': '15 day Prediction from 30 day Window', 'folder':'30daysto15days', 'T':30, 'HORIZON': 15, 'reservoir': 'krs'},
    # {'number': 3, 'title': '30 day Prediction from 30 day Window', 'folder':'30daysto30days', 'T':30, 'HORIZON': 30, 'reservoir': 'krs','model type': 'LSTM - Deep Learning Model','training loss' : 0.0049 , 'validation loss': 0.0084},
    # {'number': 4, 'title': '30 day Prediction from 60 day Window', 'folder':'60daysto30days', 'T':60, 'HORIZON': 30, 'reservoir': 'krs'},
    # {'number': 5, 'title': '30 day Prediction from 90 day Window', 'folder':'90daysto30days', 'T':90, 'HORIZON': 30, 'reservoir': 'krs'},
    # {'number': 6, 'title': '60 day Prediction from 60 day Window', 'folder':'60daysto60days', 'T':60, 'HORIZON': 60, 'reservoir': 'krs'},
    # {'number': 7, 'title': '90 day Prediction from 90 day Window', 'folder':'90daysto90days', 'T':90, 'HORIZON': 90, 'reservoir': 'krs'},
    #{'number': 8, 'title': '90 day Prediction from 30 day Weather forecast', 'folder':'30daysto1day_only_weather', 'T':30, 'HORIZON': 1, 'reservoir': 'krs', 'onlyweather':True}
]
