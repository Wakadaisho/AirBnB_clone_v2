#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls:
            temp = {}
            for key, value in FileStorage.__objects.items():
                if key.split(".")[0] == cls:
                    temp[key] = value
            return temp
        return FileStorage.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        class_name = obj.__class__.__name__
        obj_key = f"{class_name}.{obj.id}"
        FileStorage.__objects[obj_key] = obj

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            for key, val in FileStorage.__objects.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

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
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    class_name = val.get('__class__')
                    if class_name in classes:
                        obj_class = classes[class_name]
                        obj = obj_class(**val)
                        obj_key = f"{class_name}.{obj.id}"
                        FileStorage.__objects[obj_key] = obj
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Delete an object from __objects"""
        if obj:
            obj_key = f"{obj.__class__.__name__}.{obj.id}"
            if obj_key in FileStorage.__objects:
                del FileStorage.__objects[obj_key]
                self.save()
