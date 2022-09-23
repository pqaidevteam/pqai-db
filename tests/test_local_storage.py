"""
Unit test for custom wrapper around local storage
"""
import unittest
import sys
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
sys.path.append(str(BASE_DIR.resolve()))

from core.local_storage_wrapper import LocalStorage
import testutil

class TestLocalStorage(unittest.TestCase):

    """Testing getting, putting, deleting and listing operations of a test file
    """

    def setUp(self):
        root = testutil.set_up_test_local_directory()
        self.storage = LocalStorage(root)

    def test_get_file(self):
        key = 'patents/US7654321B2.json'
        contents = self.storage.get(key)
        self.assertIsInstance(contents, bytes)
        self.assertGreater(len(contents), 0)

        data = json.loads(contents)
        self.assertEqual(data['publicationNumber'], 'US7654321B2')

    def test_error_when_reading_non_existing_file(self):
        invalid_key = 'patents/arbitrary.json'
        def attempt():
            self.storage.get(invalid_key)
        self.assertRaises(FileNotFoundError, attempt)

    def test_put_and_delete_file(self):
        key = 'patents/US7654321B2.json'
        contents = self.storage.get(key)

        new_key = 'patents/new.json'
        self.storage.put(new_key, contents)

        retrieved = self.storage.get(new_key)
        self.assertEqual(retrieved, contents)

        self.storage.delete(new_key)

        def attempt():
            self.storage.get(new_key)
        self.assertRaises(FileNotFoundError, attempt)

    def test_list_files(self):
        prefix = 'patents/US'
        matches = self.storage.list(prefix)
        self.assertIs(type(matches), list)
        self.assertGreater(len(matches), 0)

        key = 'patents/notexist'
        output = self.storage.list(key)
        self.assertEqual(len(output), 0)


if __name__ == "__main__":
    unittest.main()
