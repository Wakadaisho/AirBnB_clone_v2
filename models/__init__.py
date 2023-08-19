#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage
from os import environ

storage = None

try:
    if environ['HBNB_TYPE_STORAGE'] == 'db':
        storage = DBStorage()
except Exception:
    storage = FileStorage()
else:
    storage = DBStorage()

storage.reload()
