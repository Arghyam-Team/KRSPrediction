from os.path import dirname, join

ROOT_DIR = dirname(dirname(__file__))

def get_full_path(*path):
    return join(ROOT_DIR, *path)