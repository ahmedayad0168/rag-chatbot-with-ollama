import pyodbc

from config import CONNECTION_STRING


def connect_db():
    return pyodbc.connect(CONNECTION_STRING)