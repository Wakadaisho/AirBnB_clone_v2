#!/usr/bin/python3
""" Module for testing file storage"""
import unittest
import MySQLdb
from models.city import City
from models.state import State
from models.engine.db_storage import DBStorage
from os import getenv
from datetime import datetime

skip = getenv("HBNB_TYPE_STORAGE", "file") != "db"


def run_db_query(query, args=None):
    """Run a db query and return the cursor results

    Args:
        query (str): sql query to run
        args (tuple): possible arguments to query

    Returns:
        list of query results
    """
    query_rows = None
    with MySQLdb.connect(host=getenv("HBNB_MYSQL_HOST"),
                         port=3306,
                         user=getenv("HBNB_MYSQL_USER"),
                         passwd=getenv("HBNB_MYSQL_PWD"),
                         db=getenv("HBNB_MYSQL_DB"),
                         charset="utf8") as conn:
        conn.autocommit(True)
        with conn.cursor() as cur:
            cur.execute(query, args)
            query_rows = cur.fetchall()
    return query_rows


@unittest.skipIf(skip, "DB storage testing")
class test_dbStorage(unittest.TestCase):
    """ Class to test the file storage method """

    @classmethod
    def setUpClass(cls):
        """Initializing storage"""
        cls.storage = DBStorage()

    @classmethod
    def tearDownClass(cls):
        """"""
        del cls.storage

    def test_new(self):
        """ New object is correctly added to session """
        self.storage.reload()
        # DB and session should be empty
        self.assertEqual(len(run_db_query("SELECT * FROM states")), 0)
        self.assertEqual(len(self.storage.all("State")), 0)

        state = State(name="Texas")
        self.storage.new(state)

        # DB should still be empty but not session
        self.assertEqual(len(run_db_query("SELECT * FROM states")), 0)
        self.assertEqual(len(self.storage.all("State")), 1)

    def test_all(self):
        """ __objects is properly returned """
        self.storage.reload()
        self.assertEqual(len(self.storage.all()), 0)
        state = State(name="Texas")
        city_1 = City(name="Dallas", state_id=state.id)
        city_2 = City(name="Austin", state_id=state.id)

        self.storage.new(state)
        self.storage.new(city_1)
        self.storage.new(city_2)

        self.assertEqual(len(self.storage.all()), 3)
        self.assertEqual(len(self.storage.all("State")), 1)
        self.assertEqual(len(self.storage.all("City")), 2)

    def test_save(self):
        """ DBStorage save method """
        self.storage.reload()
        state = State(name="Texas")
        self.storage.new(state)
        before = run_db_query("SELECT * FROM states")
        self.storage.save()
        after = run_db_query("SELECT * FROM states")
        self.assertEqual(len(after) - len(before), 1)

    def test_reload(self):
        """ DB is successfully reloaded to session """
        self.storage.reload()
        self.assertEqual(len(self.storage.all()), 0)
        run_db_query("""INSERT INTO states(id, name,
                                           created_at, updated_at)
                     VALUES
                     ("1", "Texas", %s, %s);
                     """, (datetime.now(), datetime.now()))
        run_db_query("""INSERT INTO cities(id, state_id, name,
                                           created_at, updated_at)
                     VALUES
                     ("1", "1", "Austin", %s, %s);
                     """, (datetime.now(), datetime.now()))
        run_db_query("""INSERT INTO cities(id, state_id, name,
                                           created_at, updated_at)
                     VALUES
                     ("2", "1", "El Paso", %s, %s);
                     """, (datetime.now(), datetime.now()))
        state_count = run_db_query("SELECT count(*) FROM states;")
        cities_count = run_db_query("SELECT count(*) FROM cities;")

        self.assertEqual(state_count[0][0], 1)
        self.assertEqual(cities_count[0][0], 2)
        self.assertEqual(len(self.storage.all()), 0)
        self.assertEqual(len(self.storage.all("State")), 0)
        self.assertEqual(len(self.storage.all("City")), 0)

        self.storage.reload()       # Loads into session (visible by .all())

        self.assertEqual(len(self.storage.all()), 3)
        self.assertEqual(len(self.storage.all("State")), 1)
        self.assertEqual(len(self.storage.all("City")), 2)

    def test_delete(self):
        """ Delete object from current session (not DB)"""
        self.storage.reload()
        self.assertEqual(len(self.storage.all()), 0)
        state = State(name="Texas")
        city_1 = City(name="Dallas", state_id=state.id)
        city_2 = City(name="Austin", state_id=state.id)

        self.storage.new(state)
        self.storage.new(city_1)
        self.storage.new(city_2)

        self.assertEqual(len(self.storage.all()), 3)
        self.assertEqual(len(self.storage.all("State")), 1)
        self.assertEqual(len(self.storage.all("City")), 2)

        # Simple independent record deletion
        self.storage.delete(city_1)
        self.assertEqual(len(self.storage.all()), 2)
        self.assertEqual(len(self.storage.all("State")), 1)
        self.assertEqual(len(self.storage.all("City")), 1)

        # Test cascade
        self.storage.delete(state)
        self.assertEqual(len(self.storage.all()), 0)
        self.assertEqual(len(self.storage.all("State")), 0)
        self.assertEqual(len(self.storage.all("City")), 0)
