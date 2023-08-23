#!/usr/bin/python3
""" """
from models.base_model import BaseModel
import unittest
import datetime
from uuid import UUID
import json
import os

isdbstorage = os.getenv("HBNB_TYPE_STORAGE", 'file') == 'db'
remove = os.remove
skipIf = unittest.skipIf
attrs = {"id": str,
         "created_at": datetime.datetime,
         "updated_at": datetime.datetime}


class test_basemodel(unittest.TestCase):
    """ """

    __cls__ = "BaseModel"

    @classmethod
    def setUpClass(cls):
        cls.obj = BaseModel()

    @classmethod
    def tearDownClass(cls):
        del cls.obj
        try:
            remove("file.json")
        except FileNotFoundError:
            pass

    def test_default(self):
        """ """
        self.assertEqual(type(self.obj), self.obj.__class__)

    def test_kwargs(self):
        """ """
        copy = self.obj.to_dict()
        new = BaseModel(**copy)
        self.assertFalse(new is self.obj)

    def test_kwargs_int(self):
        """ """
        copy = self.obj.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            BaseModel(**copy)

    @skipIf(isdbstorage and __cls__ == "BaseModel", "No BaseModel in DB")
    def test_save(self):
        """ Testing save """
        self.obj.save()
        key = self.obj.__class__.__name__ + "." + self.obj.id
        with open('file.json', 'r') as f:
            j = json.load(f)
            self.assertEqual(j[key], self.obj.to_dict())

    def test_str(self):
        """ """
        self.assertEqual(str(self.obj), '[{}] ({}) {}'.format(
            self.obj.__class__.__name__, self.obj.id,
            self.obj.__dict__))

    def test_todict(self):
        """ """
        n = self.obj.to_dict()
        self.assertEqual(self.obj.to_dict(), n)

    def test_kwargs_none(self):
        """ """
        n = {None: None}
        with self.assertRaises(TypeError):
            self.obj.__class__(**n)

    @skipIf(isdbstorage, "File storage test")
    def test_kwargs_one(self):
        """ """
        n = {'Name': 'test'}
        with self.assertRaises(KeyError):
            self.obj.__class__(**n)

    def test_id(self):
        """ """
        self.assertEqual(type(self.obj.id), str)

    def test_created_at(self):
        """ """
        self.assertEqual(type(self.obj.created_at), datetime.datetime)

    @skipIf(isdbstorage, "File storage test")
    def test_updated_at(self):
        """ """
        self.assertEqual(type(self.obj.updated_at), datetime.datetime)
        new = BaseModel(**(self.obj.to_dict()))
        self.assertFalse(new.created_at == new.updated_at)
