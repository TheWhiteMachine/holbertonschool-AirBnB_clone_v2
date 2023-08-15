#!/usr/bin/python3
"""comment"""
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv


class DBStorage:
    """"""
    __engine = None
    __session = None

    def __init__(self):
        """Constructor. Set up the DB connection"""
        user = getenv('HBNB_MYSQL_USER')
        pwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine(
            f'mysql+mysqldb://{user}:{pwd}@{host}/{db}',
            pool_pre_ping=True)
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the current database session,
        get all objects stored in the database for a specific
        class or for all classes"""

        directory = {}
        classes = [State, City, User, Place, Review, Amenity]

        if cls is None:
            for cls in classes:
                objects = self.__session.query(cls).all()
                for obj in objects:
                    key = f'{obj.__class__.__name__}.{obj.id}'
                    directory[key] = obj
            return directory
        elif cls in classes:
            objects = self.__session.query(cls).all()
            for obj in objects:
                key = f'{obj.__class__.__name__}.{obj.id}'
                directory[key] = obj
            return directory
        else:
            return {}

    def new(self, obj):
        """add the object to the current database session"""
        if obj:
            self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database"""
        Base.metadata.create_all(self.__engine)
        my_session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(my_session)
        self.__session = Session()

    def close(self):
        """Close the session"""
        self.__session.close()
