#!/usr/bin/python3
""" Place Module for HBNB project """
from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship

place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60),
                             ForeignKey('places.id'), nullable=False),
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id'), nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    city_id = ""
    user_id = ""
    name = ""
    description = ""
    number_rooms = 0
    number_bathrooms = 0
    max_guest = 0
    price_by_night = 0
    latitude = 0.0
    longitude = 0.0
    amenity_ids = []

    @property
    def reviews(self):
        """The reviews getter."""
        from models import storage
        return [review for review in storage.all("Review")
                if review.place_id == self.id]

    @property
    def amenities(self):
        """The amenity getter."""
        from models import storage
        return [amenity for amenity in storage.all("Amenity")
                if amenity.id in self.amenity_ids]

    @amenities.setter
    def amenities(self, value):
        if (type(value) == type(self)):
            self.amenity_ids.append(self.id)

    if getenv("HBNB_TYPE_STORAGE") == 'db':
        city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        amenities = relationship('Amenity',
                                 secondary=place_amenity,
                                 back_populates="place_amenities",
                                 viewonly=False)
        reviews = relationship("Review",
                               backref="place",
                               cascade="all, delete, delete-orphan")
