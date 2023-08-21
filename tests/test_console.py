#!/usr/bin/python3

"""
These are tests for the HBNBCommand class(console.py)
"""

import os
import uuid
from unittest import TestCase, skipIf
from unittest.mock import patch
from console import HBNBCommand as Bnb
from models import storage
from io import StringIO

isdbstorage = os.getenv('HBNB_TYPE_STORAGE', 'file') == 'db'


class TestConsole(TestCase):
    """
    Tests:
        - Intialization
        - quit
        - EOF
        - create
        - show
        - destroy
        - all
        - update
    """

    @classmethod
    def setUpClass(cls):
        """Set up tests"""
        cls.errors = ["** class name missing **\n",
                      "** class doesn't exist **\n",
                      "** instance id missing **\n",
                      "** no instance found **\n",
                      "** attribute name missing **\n",
                      "** value missing **\n"]
        cls.classes = ["BaseModel", "User", "State",
                       "City", "Amenity", "Place", "Review"]
        try:
            os.remove("file.json")
        except Exception:
            pass

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove("file.json")
        except Exception:
            pass

    def tearDown(self):
        storage.objects = {}
        try:
            os.remove("file.json")
        except Exception:
            pass

    def _run(self, *args, **kwargs):
        "Execute a command and get back the output"
        with patch("sys.stdout", new=StringIO()) as f:
            return Bnb().onecmd(*args) or f.getvalue()

    def test_init(self):
        """
        Test for init method
        """
        hbnb = Bnb()
        self.assertEqual(hbnb.prompt, "(hbnb) ")

    def test_quit(self):
        """
        Test for quit command
        """
        self.assertTrue(self._run("quit"))

    def test_eof(self):
        """
        Test for EOF command
        """
        self.assertTrue(self._run("EOF"))

    def test_emptyline(self):
        """
        Test for empty line
        """
        self.assertEqual(self._run("\n"), '')

    def test_help(self):
        """
        Test for help command
        """
        output = ('\nDocumented commands (type help <topic>):\n'
                  '========================================\n'
                  'EOF  all  count  create  destroy  help  quit  show  update'
                  '\n\n')
        self.assertEqual(self._run("help"), output)

    @skipIf(isdbstorage, "File storage testing")
    def test_create(self):
        """
        Test for create method error output
        """
        # Catch errors
        self.assertIn(self._run("create"), self.errors)
        self.assertIn(self._run("create Nairobi"), self.errors)

        for model in self.classes:
            output = self._run(f"create {model}").strip()
            self.assertTrue(uuid.UUID(output))
        for model in self.classes:
            output = self._run(f"create {model}").strip()
            self.assertTrue(uuid.UUID(output))

    @skipIf(isdbstorage, "File storage testing")
    def test_show(self):
        """
        Test for show
        """
        # Catch errors
        self.assertIn(self._run("show"), self.errors)
        self.assertIn(self._run("show Name"), self.errors)
        self.assertIn(self._run("show City id"), self.errors)

        for model in self.classes:
            id = self._run(f"create {model}").strip()
            # dot notation
            output = self._run(f'show {model} "{id}"').strip()
            self.assertNotIn(output, self.errors)
            self.assertTrue("Unknown syntax:" not in output)
            self.assertNotEqual(output, '')
            # default notation
            output = self._run(f'show {model} {id}').strip()
            self.assertNotIn(output, self.errors)
            self.assertTrue("Unknown syntax:" not in output)
            self.assertNotEqual(output, '')

    @skipIf(isdbstorage, "File storage testing")
    def test_all(self):
        """
        Test for all
        """
        # Catch rrors
        self.assertIn(self._run("all Mombasa"), self.errors)

        # Empty case
        output = self._run('all').strip()
        self.assertEqual(output, '[]')

        # Create test instances
        for model in self.classes:
            self._run(f'create {model} {id}').strip()

        # All instances
        output = self._run('all').strip()
        self.assertNotIn(output, self.errors)
        self.assertTrue("Unknown syntax:" not in output)
        self.assertNotEqual(output, '[]')

        # Per instance type
        for model in self.classes:
            # dot notation
            output = self._run(f'all {model}').strip()
            self.assertNotIn(output, self.errors)
            self.assertTrue("Unknown syntax:" not in output)
            self.assertNotEqual(output, '[]')
            # default notation
            output = self._run(f'all {model}').strip()
            self.assertNotIn(output, self.errors)
            self.assertTrue("Unknown syntax:" not in output)
            self.assertNotEqual(output, '[]')

    @skipIf(isdbstorage, "File storage testing")
    def test_count(self):
        """
        Test for count
        """
        initial_counts = []
        later_counts = []
        # No created instances, initial 0
        for model in self.classes:
            # dot notation
            output = int(self._run(f'count {model}').strip())
            initial_counts.append(output)

        # Create test instances
        for model in self.classes:
            self._run(f'create {model}').strip()
            output = int(self._run(f'count {model}').strip())
            later_counts.append(output - 1)

        self.assertListEqual(initial_counts, later_counts)

    @skipIf(isdbstorage, "File storage testing")
    def test_destroy(self):
        """
        Test for destroy
        """
        instances = {}
        initial_counts = []
        later_counts = []
        N = 2
        # Check errors
        self.assertIn(self._run("destroy"), self.errors)
        self.assertIn(self._run("destroy City"), self.errors)
        self.assertIn(self._run("destroy State sochi"), self.errors)

        # Create test instances (2 each)
        for model in self.classes:
            instances[model] = []
            for _ in range(N):
                instances[model].append(self._run(f'create {model}').strip())

        for model in self.classes:
            initial_counts.append(int(self._run(f'count {model}').strip()))

        for model in self.classes:
            for i in range(N):
                id = instances[model][i]
                output = self._run(f'destroy {model} {id}')
                self.assertNotIn(output, self.errors)
                self.assertTrue("Unknown syntax:" not in output)

        for model in self.classes:
            later_counts.append(int(self._run(f'count {model}').strip()) + N)

        self.assertListEqual(initial_counts, later_counts)

    @skipIf(isdbstorage, "File storage testing")
    def test_update(self):
        """
        Test for update command error message
        """
        instances = {}

        # Check errors
        self.assertIn(self._run("update"), self.errors)
        self.assertIn(self._run("update State"), self.errors)
        self.assertIn(self._run("update State id"), self.errors)
        id = self._run("create State")
        self.assertIn(self._run(f"update State {id}"), self.errors)
        self.assertIn(self._run(f"update State {id} attr"), self.errors)

        # Error check cleanup
        self._run(f"destroy State {id}")

        # Create test instances (2 each), add attributes
        for model in self.classes:
            id = self._run(f'create {model}').strip()
            # default notation
            self._run(f'update {model} {id} arg_float 3.14')
            self._run(f'update {model} {id} arg_int 42')

            # dot notation
            self._run(f'update {model} {id} arg_string "Miles"')
            instances[model] = id

        for model in self.classes:
            output = self._run(f'show {model} {instances[model]}')
            self.assertIn("'arg_float': 3.14", output)
            self.assertIn("'arg_int': 42", output)
            self.assertIn("'arg_string': 'Miles'", output)
