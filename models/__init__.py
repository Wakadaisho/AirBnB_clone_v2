#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
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

__all__ = ["User", "Place", "State", "City", "Amenity", "Review", "storage"]
