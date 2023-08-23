#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import (test_basemodel,
                                               isdbstorage,
                                               remove,
                                               skipIf)
from models.place import Place
from models.user import User
from models.city import City
from models.state import State
from models import storage


class test_Place(test_basemodel):
    """ """

    @classmethod
    def setUpClass(cls):
        if (isdbstorage):
            cls.user = User(email="first.last@email.com",
                            password="thisbemysecret",
                            first_name="first",
                            last_name="last")
            cls.state = State(name="Texas")
            cls.city = City(name="Dallas",
                            state_id=cls.state.id)
            cls.obj = Place(name="Silky Woods",
                            description="High-class Estate",
                            number_rooms=6,
                            number_bathrooms=5,
                            max_guest=7,
                            price_by_night=100,
                            latitude=30.154,
                            longitude=2.343,
                            user_id=cls.user.id,
                            city_id=cls.city.id)
        else:
            cls.obj = Place()

    @classmethod
    def tearDownClass(cls):
        del cls.obj
        try:
            remove("file.json")
        except FileNotFoundError:
            pass

    def test_city_id(self):
        """ """
        self.assertEqual(type(self.obj.city_id), str)

    def test_user_id(self):
        """ """
        self.assertEqual(type(self.obj.user_id), str)

    def test_name(self):
        """ """
        self.assertEqual(type(self.obj.name), str)

    def test_description(self):
        """ """
        self.assertEqual(type(self.obj.description), str)

    def test_number_rooms(self):
        """ """
        self.assertEqual(type(self.obj.number_rooms), int)

    def test_number_bathrooms(self):
        """ """
        self.assertEqual(type(self.obj.number_bathrooms), int)

    def test_max_guest(self):
        """ """
        self.assertEqual(type(self.obj.max_guest), int)

    def test_price_by_night(self):
        """ """
        self.assertEqual(type(self.obj.price_by_night), int)

    def test_latitude(self):
        """ """
        self.assertEqual(type(self.obj.latitude), float)

    def test_longitude(self):
        """ """
        self.assertEqual(type(self.obj.longitude), float)

    def test_amenity_ids(self):
        """ """
        self.assertEqual(type(self.obj.amenity_ids), list)

    @skipIf(not isdbstorage, "DB storage test")
    def test_db_and_attributes(self):
        """Test: Place attributes"""
        self.assertEqual(self.obj.name, "Silky Woods")
        self.assertEqual(self.obj.description, "High-class Estate")
        self.assertEqual(self.obj.number_rooms, 6)
        self.assertEqual(self.obj.number_bathrooms, 5)
        self.assertEqual(self.obj.max_guest, 7)
        self.assertEqual(self.obj.price_by_night, 100)
        self.assertEqual(self.obj.latitude, 30.154)
        self.assertEqual(self.obj.longitude, 2.343)
        self.assertEqual(self.obj.price_by_night, 100)
        self.assertEqual(self.obj.user_id, self.user.id)
        self.assertEqual(self.obj.city_id, self.city.id)

        storage.reload()
        storage.new(self.user)
        storage.new(self.state)
        storage.new(self.city)
        storage.new(self.obj)
        storage.save()
