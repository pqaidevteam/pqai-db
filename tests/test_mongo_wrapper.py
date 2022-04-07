"""
Unit tests for MongoDB wrapper
"""
import unittest
import sys
import json
from pathlib import Path
import pymongo

TEST_DIR = Path(__file__).parent
BASE_DIR = Path(__file__).parent.parent
sys.path.append(str(BASE_DIR.resolve()))

#pylint: disable=wrong-import-position
from core.mongo_wrapper import Mongo

class TestLocalStorage(unittest.TestCase):

    """Test get, put, delete, and list docs in/from Mongo DB
    """

    def setUp(self):
        """Initial setup
        """
        self.mongodb = Mongo()
        self.pn = 'US7654321B2'
        with open(str((TEST_DIR / f'{self.pn}.json').resolve())) as f:
            data = json.load(f)
        try:
            self.mongodb.put(self.pn, data)
        except pymongo.errors.DuplicateKeyError:
            pass # document pre-exists

    def test_can_add_get_delete_doc(self):
        """Test whether documents can be added/deleted/retrieved/listed
        """
        doc = self.mongodb.get(self.pn)
        self.assertIsInstance(doc, dict)
        self.assertIn('publicationNumber', doc)
        self.assertEqual(doc['publicationNumber'], self.pn)

        self.mongodb.delete(self.pn)

        attempt = lambda: self.mongodb.get(self.pn)
        self.assertRaises(attempt)

        with open(str((TEST_DIR / f'{self.pn}.json').resolve())) as f:
            data = json.load(f)
        self.mongodb.put(self.pn, data)

        ls = self.mongodb.list('US7654321B2')
        self.assertIsInstance(ls, list)
        self.assertGreater(len(ls), 0)


if __name__ == '__main__':
    unittest.main()
