#!/usr/bin/python3
"""This module defines a class to manage DB storage for hbnb clone"""
from os import getenv
from sqlalchemy import create_engine, orm
from models.base_model import Base
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
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(getenv('HBNB_MYSQL_USER'),
                                              getenv('HBNB_MYSQL_PWD'),
                                              getenv('HBNB_MYSQL_HOST'),
                                              getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)
        if (getenv('HBNB_ENV') == 'test' and
                getenv('HBNB_TYPE_STORAGE', 'file') == 'db'):
            # Drop all tables
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        f = {}

        classes = {
                'User': User, 'Place': Place,
                'State': State, 'City': City, 'Amenity': Amenity,
                'Review': Review
                }
        if cls:
            for row in self.__session.query(classes[cls]).all():
                f.update({f"{row.to_dict()['__class__']}.{row.id}": row})
        else:
            for cls in classes.values():
                for row in self.__session.query(cls).all():
                    f.update({f"{row.to_dict()['__class__']}.{row.id}": row})
        return f

    def new(self, obj):
        """Adds new object to DB storage"""
        self.__session.add(obj)

    def save(self):
        """Saves (commits) changes to the DB __session"""
        self.__session.commit()

    def reload(self):
        """Loads storage data from DB __engine"""
        Base.metadata.create_all(self.__engine)
        self.__session = orm.scoped_session(
                orm.sessionmaker(bind=self.__engine,
                                 expire_on_commit=False))()

    def delete(self, obj=None):
        """Delete an object from __session"""
        if obj:
            self.__session.delete(obj)
