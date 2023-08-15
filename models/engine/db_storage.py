#!/usr/bin/python3
"""" setting de db class"""


import sqlalchemy as db
from sqlalchemy import create_engine
import os
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import MetaData
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models.base_model import Base


class DBStorage():
    """ this class manage the DB"""

    __engine = None
    __session = None

    def __init__(self):
        """" set the dn engine for swl alchemy
        and erase all tables if test is happening """

        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".format(
            os.getenv("HBNB_MYSQL_USER"),
            os.getenv("HBNB_MYSQL_PWD"),
            os.getenv("HBNB_MYSQL_HOST"),
            os.getenv("HBNB_MYSQL_DB"),
            pool_pre_ping=True))
        if os.getenv('HBNB_ENV') == 'test':
            m = MetaData()
            m.reflect(self.__engine)
            m.drop_all(self.__engine)

    def all(self, cls=None):
        """" list all tables or all from one specific askedd in cls"""
        objects = {}
        if cls:
            objects = self.__session.query(cls).all()
        else:
            objects = self.__session.query(User).all()
            objects.extend(self.__session.query(State).all())
            objects.extend(self.__session.query(City).all())
            objects.extend(self.__session.query(Amenity).all())
            objects.extend(self.__session.query(Place).all())
            objects.extend(self.__session.query(Review).all())
        result_dict = {"{}.{}".format(obj.__class__.__name__,
                                      obj.id): obj for obj in objects}
        return result_dict

    def new(self, obj):
        """" add an object to the database """
        self.__session.add(obj)

    def save(self):
        """ commit all changes """
        self.__session.commit()

    def delete(self, obj=None):
        """ delete from current database obj if nnot one"""
        if obj:
            self.__session.delete(obj)
            self.__session.save()

    def reload(self):
        """ create tables in DB and session """
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(
            sessionmaker(bind=self.__engine,
                         expire_on_commit=False))
        self.__session = Session()

    def close(self):
        self.__session.remove()
