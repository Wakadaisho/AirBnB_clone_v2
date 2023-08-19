#!/usr/bin/python3
"""This module defines a class to manage DB storage for hbnb clone"""
from os import getenv
from sqlalchemy import create_engine, inspect, orm
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import Base, BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

class DBStorage:
    """This class manages storage of hbnb models stored in a MySQL DB"""
    __engine = None
    __session = None

    def __init__(self):
        DBStorage.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                           .format(getenv('HBNB_MYSQL_USER'),
                                   getenv('HBNB_MYSQL_PWD'),
                                   getenv('HBNB_MYSQL_HOST'),
                                   getenv('HBNB_MYSQL_DB')),
                           pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            # Drop all tables
            Base.metadata.drop_all(DBStorage.__engine)
            pass
    
    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        metadata = inspect(DBStorage.__engine)
        records = {}
        print("metadata", metadata.get_table_names())

        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        if (cls):
            for row in DBStorage.__session.query(classes[cls]).all():
              records.update({row.to_dict()['__class__'] + '.' + row.id: row})
        else:
            for cls in classes.values():
                for row in DBStorage.__session.query(cls).all():
                  records.update({row.to_dict()['__class__'] + '.' + row.id: row})
        return records


    def new(self, obj):
        """Adds new object to DB storage"""
        print("adding new", obj)
        print(obj.to_dict())
        self.__session.add(obj)

    def save(self):
        """Saves (commits) changes to the DB __session"""
        print("Saving new")
        self.__session.commit()

    def reload(self):
        """Loads storage dictionary from DB __engine"""
        print("Reloading new")
        Base.metadata.create_all(self.__engine)
        State.__table__.create(bind=DBStorage.__engine, checkfirst=True)
        City.__table__.create(bind=DBStorage.__engine, checkfirst=True)
        self.__session = orm.scoped_session(
                orm.sessionmaker(bind=self.__engine, 
                                 expire_on_commit=False))()

    def delete(self, obj=None):
        """Delete an object from __session"""
        if obj:
           self.__session.query(obj).delete()
