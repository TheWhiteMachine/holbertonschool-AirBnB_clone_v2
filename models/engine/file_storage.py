#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls is None:
            return self.__objects
        else:
            list_of_obj = {}
            for key, val in self.__objects.items():
                if isinstance(val, cls):
                    list_of_obj[key] = val
            return list_of_obj

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as theFile:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, theFile)

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
            'BaseModel': BaseModel, 'User': User, 'Place': Place,
            'State': State, 'City': City, 'Amenity': Amenity,
            'Review': Review
        }
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as theFile:
                temp = json.load(theFile)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """ Delete a None Object """
        objClass = str(obj.__class__.__name__)
        if obj is not None:
            objKey = objClass + "." + str(obj.id)
            if objKey in self.__objects:
                del self.__objects[objKey]

    def close(self):
        """ call reaload """
        return self.reload()
