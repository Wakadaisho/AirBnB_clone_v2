#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import (test_basemodel, isdbstorage,
                                               skipIf, attrs, remove)
from models.base_model import BaseModel
from models.state import State

state_attrs = {"name": str}


class test_state(test_basemodel):
    """ """

    @classmethod
    def setUpClass(cls):
        '''
            Sets up test State class
        '''
        cls.state = State()

    @classmethod
    def tearDownClass(cls):
        '''
            Tears down unittest
        '''
        del cls.state
        try:
            remove("file.json")
        except FileNotFoundError:
            pass

    @skipIf(isdbstorage, "File storage testing")
    def test_name(self):
        """ """
        self.assertEqual(type(self.state.name), str)

    def test_inheritance(self):
        """Test: State inherits from BaseModel"""
        self.assertIsInstance(self.state, BaseModel)
        self.assertTrue(all([val in dir(self.state) for val in attrs]),
                        "Found value not inherited")

    def test_table_name(self):
        """Test: State represents the table 'states'"""
        self.assertEqual(self.state.__tablename__, "states")

    @skipIf(isdbstorage, "File storage testing")
    def test_attributes(self):
        """Test: State attributes"""
        self.assertIsInstance(self.state, BaseModel)
        self.assertTrue(all([val in dir(self.state) for val in state_attrs]),
                        "Found value not inherited")
        # test if attributes have been initialized to defaults
        self.assertEqual(self.state.name, "")
