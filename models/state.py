#!/usr/bin/python3
""" State Module for HBNB project """
from os import getenv
from models.base_model import BaseModel, Base
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
        return [city for city in storage.all("City")
                if city.state_id == self.id]

    if getenv("HBNB_TYPE_STORAGE") == 'db':
        name = Column(String(128), nullable=False)
        cities = relationship("City",
                              backref="state",
                              cascade="all, delete-orphan",
                              lazy="dynamic")
