#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import (test_basemodel, isdbstorage,
                                               skipIf, attrs, remove)
from models.base_model import BaseModel, Base
from models.city import City
from models.state import State
from models import storage

city_attrs = {"name": str, "state_id": str}


class test_City(test_basemodel):
    """ """

    @classmethod
    def setUpClass(cls):
        if (isdbstorage):
            cls.state = State(name="Texas")
            cls.obj = City(name="Dallas",
                           state_id=cls.state.id)
        else:
            cls.obj = City()

    @classmethod
    def tearDownClass(cls):
        try:
            remove("file.json")
        except FileNotFoundError:
            pass

    @skipIf(isdbstorage, "File storage test")
    def test_state_id(self):
        """ """
        self.assertEqual(type(self.obj.state_id), str)

    def test_name(self):
        """ """
        self.assertEqual(type(self.obj.name), str)

    def test_inheritance(self):
        """Test: City inherits from BaseModel"""
        self.assertIsInstance(self.obj, BaseModel)
        self.assertTrue(all([val in dir(self.obj) for val in attrs]),
                        "Found value not inherited")

    def test_table_name(self):
        """Test: City represents the table 'cities'"""
        self.assertEqual(self.obj.__tablename__, "cities")

    @skipIf(isdbstorage, "File storage test")
    def test_attributes(self):
        """Test: City attributes"""
        self.assertIsInstance(self.obj, BaseModel)
        self.assertTrue(all([val in dir(self.obj) for val in city_attrs]),
                        "Found value not inherited")
        # test if attributes have been initialized to defaults
        self.assertEqual(self.obj.state_id, "")
        self.assertEqual(self.obj.name, "")

    @skipIf(not isdbstorage, "DB storage test")
    def test_db_and_attributes(self):
        """Test: City attributes"""

        self.assertEqual(self.obj.state_id, self.state.id)
        self.assertEqual(self.obj.name, "Dallas")

        storage.reload()
        storage.new(self.state)
        storage.new(self.obj)
        storage.save()
