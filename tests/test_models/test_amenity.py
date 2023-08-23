#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import (test_basemodel,
                                               skipIf,
                                               remove,
                                               isdbstorage)
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models import storage


class test_Amenity(test_basemodel):
    """ """

    @classmethod
    def setUpClass(cls):
        if (isdbstorage):
            cls.host = User(email="first.last@email.com",
                            password="thisbemysecret",
                            first_name="first",
                            last_name="last")
            cls.host_2 = User(email="second.last@email.com",
                              password="thisbemysecret2",
                              first_name="second",
                              last_name="last")
            cls.state = State(name="Texas")
            cls.city = City(name="Dallas",
                            state_id=cls.state.id)
            cls.state_2 = State(name="New Jersey")
            cls.city_2 = City(name="New Jersey",
                              state_id=cls.state_2.id)
            cls.estate = Place(name="Silky Woods",
                               description="High-class Estate",
                               number_rooms=6,
                               number_bathrooms=5,
                               max_guest=7,
                               price_by_night=100,
                               latitude=30.154,
                               longitude=2.343,
                               user_id=cls.host.id,
                               city_id=cls.city.id)
            cls.house = Place(name="Sigma Abodes",
                              description="Suburb",
                              number_rooms=4,
                              number_bathrooms=2,
                              max_guest=4,
                              price_by_night=50,
                              user_id=cls.host_2.id,
                              city_id=cls.city_2.id)
            cls.gym = Amenity(name="Gym")
            cls.pool = Amenity(name="Swimming Pool")
            cls.estate.amenities.append(cls.gym)
            cls.estate.amenities.append(cls.pool)
            cls.house.amenities.append(cls.gym)
            cls.obj = cls.gym
        else:
            cls.obj = Amenity()

    @classmethod
    def tearDownClass(cls):
        try:
            remove("file.json")
        except FileNotFoundError:
            pass

    def test_name2(self):
        """ """
        self.assertEqual(type(self.obj.name), str)

    @skipIf(not isdbstorage, "DB storage test")
    def test_db_and_attributes(self):
        """Test: Amenity attributes"""

        self.assertEqual(self.gym.name, "Gym")
        self.assertEqual(self.pool.name, "Swimming Pool")
        self.assertListEqual(self.gym.place_amenities,
                             [self.estate, self.house])
        self.assertListEqual(self.pool.place_amenities, [self.estate])

        storage.reload()
        storage.new(self.host)
        storage.new(self.host_2)
        storage.new(self.state)
        storage.new(self.city)
        storage.new(self.state_2)
        storage.new(self.city_2)
        storage.new(self.estate)
        storage.new(self.house)
        storage.save()
