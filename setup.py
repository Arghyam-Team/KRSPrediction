from os.path import dirname, join

ROOT_DIR = dirname(dirname(__file__))

def get_full_path(*path):
    return join(ROOT_DIR, *path)

MODELS = [
    {'number': 1, 'title': 'One day Prediction from 30 day Window', 'folder':'30day_to_1day', 'T':30, 'HORIZON': 1, 'reservoir': 'krs'}
]