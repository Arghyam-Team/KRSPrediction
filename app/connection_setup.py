## Setup connection
import streamlit as st
import sqlite3
from sqlite3 import Connection
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

URI_SQLITE_DB = os.path.join(dir_path, "../data/pythonsqlite.db")

@st.cache(hash_funcs={Connection: id})
def get_connection(path: str):
    """Put the connection in cache to reuse if path does not change between Streamlit reruns.
    NB : https://stackoverflow.com/questions/48218065/programmingerror-sqlite-objects-created-in-a-thread-can-only-be-used-in-that-sa
    """
    return sqlite3.connect(path, check_same_thread=False)

CONN = get_connection(URI_SQLITE_DB)

