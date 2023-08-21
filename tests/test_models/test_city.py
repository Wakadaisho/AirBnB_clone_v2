#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import (test_basemodel, isdbstorage,
                                               skipIf, attrs, remove)
from models.base_model import BaseModel, Base
from models.city import City

city_attrs = {"name": str, "state_id": str}


class test_City(test_basemodel):
    """ """

    @classmethod
    def setUpClass(cls):
        '''
            Sets up test City class
        '''
        cls.city = City()

    @classmethod
    def tearDownClass(cls):
        '''
            Tears down unittest
        '''
        del cls.city
        try:
            remove("file.json")
        except FileNotFoundError:
            pass

    @skipIf(isdbstorage, "File storage testing")
    def test_state_id(self):
        """ """
        self.assertEqual(type(self.city.state_id), str)

    @skipIf(isdbstorage, "File storage testing")
    def test_name(self):
        """ """
        self.assertEqual(type(self.city.name), str)

    def test_inheritance(self):
        """Test: City inherits from BaseModel"""
        self.assertIsInstance(self.city, BaseModel)
        self.assertTrue(all([val in dir(self.city) for val in attrs]),
                        "Found value not inherited")

    def test_table_name(self):
        """Test: City represents the table 'cities'"""
        self.assertEqual(self.city.__tablename__, "cities")

    @skipIf(isdbstorage, "File storage testing")
    def test_attributes(self):
        """Test: City attributes"""
        self.assertIsInstance(self.city, BaseModel)
        self.assertTrue(all([val in dir(self.city) for val in city_attrs]),
                        "Found value not inherited")
        # test if attributes have been initialized to defaults
        self.assertEqual(self.city.state_id, "")
        self.assertEqual(self.city.name, "")
