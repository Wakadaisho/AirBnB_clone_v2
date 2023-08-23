#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import (test_basemodel,
                                               skipIf,
                                               remove,
                                               isdbstorage)
from models.user import User
from models import storage


class test_User(test_basemodel):
    """ """

    @classmethod
    def setUpClass(cls):
        if (isdbstorage):
            cls.obj = User(email="first.last@email.com",
                           password="thisbemysecret",
                           first_name="first",
                           last_name="last")

        else:
            cls.obj = User()

    @classmethod
    def tearDownClass(cls):
        del cls.obj
        try:
            remove("file.json")
        except FileNotFoundError:
            pass

    def test_first_name(self):
        """ """
        self.assertEqual(type(self.obj.first_name), str)

    def test_last_name(self):
        """ """
        self.assertEqual(type(self.obj.last_name), str)

    def test_email(self):
        """ """
        self.assertEqual(type(self.obj.email), str)

    def test_password(self):
        """ """
        self.assertEqual(type(self.obj.password), str)

    @skipIf(not isdbstorage, "DB storage test")
    def test_db_and_attributes(self):
        """Test: User attributes"""
        self.assertEqual(self.obj.email, "first.last@email.com")
        self.assertEqual(self.obj.password, "thisbemysecret")
        self.assertEqual(self.obj.first_name, "first")
        self.assertEqual(self.obj.last_name, "last")

        storage.reload()
        storage.new(self.obj)
        storage.save()
