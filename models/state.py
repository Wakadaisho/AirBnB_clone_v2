#!/usr/bin/python3
""" State Module for HBNB project """
from os import getenv
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = ""

    @property
    def cities(self):
        """The cities getter."""
        from models import storage
        return [city for _, city in storage.all(City).items()
                if city.state_id == self.id]

    if getenv("HBNB_TYPE_STORAGE") == 'db':
        name = Column(String(128), nullable=False)
        cities = relationship("City",
                              backref="state",
                              cascade="all, delete-orphan")
