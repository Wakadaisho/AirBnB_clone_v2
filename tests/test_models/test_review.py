#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import (test_basemodel,
                                               skipIf,
                                               remove,
                                               isdbstorage)
from models.review import Review
from models.place import Place
from models.user import User
from models.state import State
from models.city import City
from models import storage


class test_review(test_basemodel):
    """ """

    @classmethod
    def setUpClass(cls):
        if (isdbstorage):
            cls.user = User(email="first.last@email.com",
                            password="thisbemysecret",
                            first_name="first",
                            last_name="last")
            cls.customer = User(email="your`.customer@email.com",
                                password="onholiday",
                                first_name="your",
                                last_name="customer")
            cls.state = State(name="Texas")
            cls.city = City(name="Dallas",
                            state_id=cls.state.id)
            cls.place = Place(name="Silky Woods",
                              description="High-class Estate",
                              number_rooms=6,
                              number_bathrooms=5,
                              max_guest=7,
                              price_by_night=100,
                              user_id=cls.user.id,
                              city_id=cls.city.id)
            cls.obj = Review(text="Nice Place",
                             place_id=cls.place.id,
                             user_id=cls.customer.id)
        else:
            cls.obj = Review()

    @classmethod
    def tearDownClass(cls):
        del cls.obj
        try:
            remove("file.json")
        except FileNotFoundError:
            pass

    def test_place_id(self):
        """ """
        self.assertEqual(type(self.obj.place_id), str)

    def test_user_id(self):
        """ """
        self.assertEqual(type(self.obj.user_id), str)

    def test_text(self):
        """ """
        self.assertEqual(type(self.obj.text), str)

    @skipIf(not isdbstorage, "DB storage test")
    def test_db_and_attributes(self):
        """Test: Review attributes"""
        self.assertEqual(self.obj.text, "Nice Place")
        self.assertEqual(self.obj.user_id, self.customer.id)
        self.assertEqual(self.obj.place_id, self.place.id)

        storage.reload()
        storage.new(self.user)
        storage.new(self.customer)
        storage.new(self.state)
        storage.new(self.city)
        storage.new(self.place)
        storage.new(self.obj)
        storage.save()
