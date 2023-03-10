#!/usr/bin/python3
<<<<<<< HEAD
"""Defines the FileStorage class."""
import json
=======
"""Module for FileStorage class"""
>>>>>>> Giddy
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
<<<<<<< HEAD
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """Represent an abstracted storage engine.

    Attributes:
        __file_path (str): The name of the file to save objects to.
        __objects (dict): A dictionary of instantiated objects.
    """
=======
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import json
import os

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class FileStorage:
    """Class for serialization and deserialization"""
>>>>>>> Giddy
    __file_path = "file.json"
    __objects = {}

    def all(self):
<<<<<<< HEAD
        """Return the dictionary __objects."""
        return FileStorage.__objects

    def new(self, obj):
        """Set in __objects obj with key <obj_class_name>.id"""
        ocname = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(ocname, obj.id)] = obj

    def save(self):
        """Serialize __objects to the JSON file __file_path."""
        odict = FileStorage.__objects
        objdict = {obj: odict[obj].to_dict() for obj in odict.keys()}
        with open(FileStorage.__file_path, "w") as f:
            json.dump(objdict, f)

    def reload(self):
        """Deserialize the JSON file __file_path to __objects, if it exists."""
        try:
            with open(FileStorage.__file_path) as f:
                objdict = json.load(f)
                for o in objdict.values():
                    cls_name = o["__class__"]
                    del o["__class__"]
                    self.new(eval(cls_name)(**o))
        except FileNotFoundError:
            return
=======
        """Return the dictionary __objects"""
        return self.__objects

    def new(self, obj):
        """ Instantiates a new object and saves it
        to the dictionary with its new key """
        key = obj.__class__.__name__ + "." + obj.id
        self.__objects[key] = obj

    def save(self):
        """ Serializes the object to the JSON file """
        json_objects = {}
        for key in self.__objects:
            json_objects[key] = self.__objects[key].to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, 'r') as f:
                jf = json.load(f)
            for key in jf:
                self.__objects[key] = classes[jf[key]["__class__"]](**jf[key])
        except:
            pass
>>>>>>> Giddy
