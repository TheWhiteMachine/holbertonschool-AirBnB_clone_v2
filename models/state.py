#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel
from models.base_model import Base
from sqlalchemy import Column, String
import os
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        name = Column(String(128), unique=True, nullable=False)
        id = Column(String(60), primary_key=True, nullable=False)
        cities = relationship("City", backref="state",
                              cascade="all, delete, delete-orphan")
    else:
        id = ""
        name = ""
        # getter

        def get_cities(self):
            from engine.file_storage import FileStorage
            from models.city import City
            list_of_cities = []
            for key in FileStorage.all(City).values():
                if key.state_id == self.id:
                    list_of_cities.append(key)
            return list_of_cities
