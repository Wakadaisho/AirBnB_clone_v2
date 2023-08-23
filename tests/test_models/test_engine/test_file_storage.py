#!/usr/bin/python3
""" Module for testing file storage"""
import unittest
from models.base_model import BaseModel
from models import storage
from models.engine.file_storage import FileStorage
import os

skip = os.getenv("HBNB_TYPE_STORAGE", "file") != "file"


@unittest.skipIf(skip, "File storage testing")
class test_fileStorage(unittest.TestCase):
    """ Class to test the file storage method """

    @classmethod
    def setUpClass(cls):
        """
            Initializing storage
        """
        cls.storage = FileStorage()

    @classmethod
    def tearDownClass(cls):
        """"""
        del cls.storage

    def setUp(self):
        """ Set up test environment """
        del_list = []
        for key in self.storage._FileStorage__objects.keys():
            del_list.append(key)
        for key in del_list:
            del self.storage._FileStorage__objects[key]

    def tearDown(self):
        """ Remove storage file at end of tests """
        try:
            os.remove("file.json")
        except Exception:
            pass

    def test_obj_list_empty(self):
        """ __objects is initially empty """
        self.assertEqual(len(self.storage.all()), 0)

    def test_new(self):
        """ New object is correctly added to __objects """
        new = BaseModel()
        self.storage.new(new)
        id = new.to_dict()["__class__"] + "." + new.to_dict()["id"]
        self.assertTrue(id in self.storage.all())

    def test_all(self):
        """ __objects is properly returned """
        new = BaseModel()
        temp = self.storage.all()
        self.assertIsInstance(temp, dict)

    def test_base_model_instantiation(self):
        """ File is not created on BaseModel save """
        new = BaseModel()
        self.assertFalse(os.path.exists("file.json"))

    def test_empty(self):
        """ Data is saved to file """
        new = BaseModel()
        thing = new.to_dict()
        new.save()
        new2 = BaseModel(**thing)
        self.assertNotEqual(os.path.getsize("file.json"), 0)

    def test_save(self):
        """ FileStorage save method """
        new = BaseModel()
        self.storage.save()
        self.assertTrue(os.path.exists("file.json"))

    def test_reload(self):
        """ Storage file is successfully loaded to __objects """
        new = BaseModel()
        self.storage.save()
        self.storage.reload()
        for obj in self.storage.all().values():
            print(obj)
            self.assertEqual(new.to_dict()["id"], obj.to_dict()["id"])

    def test_reload_empty(self):
        """ Load from an empty file """
        with open("file.json", "w") as f:
            pass
        with self.assertRaises(ValueError):
            self.storage.reload()

    def test_reload_from_nonexistent(self):
        """ Nothing happens if file does not exist """
        self.assertEqual(self.storage.reload(), None)

    def test_base_model_save(self):
        """ BaseModel save method calls storage save """
        new = BaseModel()
        new.save()
        self.assertTrue(os.path.exists("file.json"))

    def test_type_path(self):
        """ Confirm __file_path is string """
        self.assertEqual(type(self.storage._FileStorage__file_path), str)

    def test_type_objects(self):
        """ Confirm __objects is a dict """
        self.assertEqual(type(self.storage.all()), dict)

    def test_key_format(self):
        """ Key is properly formatted """
        new = BaseModel()
        _id = new.to_dict()["id"]
        for key in self.storage.all().keys():
            self.assertEqual(key, "BaseModel" + "." + _id)

    def test_storage_var_created(self):
        """ FileStorage object storage created """
        self.assertEqual(type(self.storage), FileStorage)
