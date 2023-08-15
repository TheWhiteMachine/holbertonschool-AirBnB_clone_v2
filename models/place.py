#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel
from models.base_model import Base
import os
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy import Table
from sqlalchemy.orm import relationship

place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60), ForeignKey(
                          'places.id'), primary_key=True, nullable=False),
                      Column('amenity_id', String(60), ForeignKey(
                          'amenities.id'), primary_key=True, nullable=False)
                      )


class Place(BaseModel, Base):
    """ A place to stay """

    __tablename__ = "places"
    if os.getenv("HBNB_TYPE_STORAGE") == "db":

        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, default=0, nullable=False)
        number_bathrooms = Column(Integer, default=0, nullable=False)
        max_guest = Column(Integer, default=0, nullable=False)
        price_by_night = Column(Integer, default=0, nullable=False)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship("Review", cascade="all,delete", backref="place")
        amenities = relationship(
            "Amenity", secondary=place_amenity, viewonly=False)
    else:
        @property
        def reviews(self):
            """"append cities that share state.id"""
            from models import storage

            reviewsOfPlace = []
            for obj in storage.all():
                if obj.__class__.__name__ == 'Review':
                    if obj.place_id == self.id:
                        reviewsOfPlace.append(obj)
            return reviewsOfPlace

        @property
        def amenities(self):
            """Getter attribute """
            from models.amenity import Amenity
            from models import storage
            amenities_list = []
            for amenity_id in self.amenity_ids:
                amenity_obj = storage.get(Amenity, amenity_id)
                if amenity_obj:
                    amenities_list.append(amenity_obj)
            return amenities_list

        @amenities.setter
        def amenities(self, obj):
            """Setter attribute """
            from models.amenity import Amenity
            if isinstance(obj, Amenity):
                self.amenity_ids.append(obj.id)
