#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import (test_basemodel, isdbstorage,
                                               skipIf, attrs, remove)
from models.base_model import BaseModel
from models.state import State
from models import storage

state_attrs = {"name": str}


class test_state(test_basemodel):
    """ """

    @classmethod
    def setUpClass(cls):
        if (isdbstorage):
            cls.obj = State(name="Texas")
        else:
            cls.obj = State()

    @classmethod
    def tearDownClass(cls):
        del cls.obj
        try:
            remove("file.json")
        except FileNotFoundError:
            pass

    def test_name(self):
        """ """
        self.assertEqual(type(self.obj.name), str)

    def test_inheritance(self):
        """Test: State inherits from BaseModel"""
        self.assertIsInstance(self.obj, BaseModel)
        self.assertTrue(all([val in dir(self.obj) for val in attrs]),
                        "Found value not inherited")

    def test_table_name(self):
        """Test: State represents the table 'states'"""
        self.assertEqual(self.obj.__tablename__, "states")

    @skipIf(isdbstorage, "File storage test")
    def test_attributes(self):
        """Test: State attributes"""
        self.assertIsInstance(self.obj, BaseModel)
        self.assertTrue(all([val in dir(self.obj) for val in state_attrs]),
                        "Found value not inherited")
        # test if attributes have been initialized to defaults
        self.assertEqual(self.obj.name, "")

    @skipIf(not isdbstorage, "DB storage test")
    def test_db_and_attributes(self):
        """Test: State attributes"""
        self.assertEqual(self.obj.name, "Texas")

        storage.reload()
        storage.new(self.obj)
        storage.save()
