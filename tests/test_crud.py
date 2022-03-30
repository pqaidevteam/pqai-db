"""Unit tests for the `crud` module

Attributes:
    BASE_DIR (TYPE): Description
    TEST_DIR (TYPE): Description
"""

# pylint: disable=C0103
import os
import unittest
import sys
from pathlib import Path

import dotenv

TEST_DIR = Path(__file__).parent
BASE_DIR = Path(__file__).parent.resolve().parent
sys.path.append(str(BASE_DIR))

from core import crud
dotenv.load_dotenv()

class TestOperations_s3(unittest.TestCase):

    """Test CRUD operations
    """

    def setUp(self):
        """Initialize example patent and application numbers

        Separate tests are written for patents and applications because their
        data is published differently by the patent offices and consequently,
        processed and stored differently.
        """
        self.pn = 'US7654321B2'
        self.app = 'US20080156487A1'
        os.environ["STORAGE"] = 's3'
    def test_get_patent(self):
        """Can retrieve a patent by its patent number?
        """
        patent = crud.get_doc(self.pn)
        self.assertIsInstance(patent, dict)
        self.assertEqual(self.pn, patent['publicationNumber'])
        self.assertIn('title', patent)
        self.assertIn('abstract', patent)
        self.assertIn('publicationDate', patent)

    def test_get_application(self):
        """Can retrieve a patent application given its publication number?
        """
        patent = crud.get_doc(self.app)
        self.assertIsInstance(patent, dict)
        self.assertEqual(self.app, patent['publicationNumber'])
        self.assertIn('title', patent)
        self.assertIn('abstract', patent)
        self.assertIn('publicationDate', patent)

    def test_list_patent_drawings(self):
        """Can list the drawings associated with a patent?
        """
        drawings = crud.list_drawings(self.pn)
        self.assertEqual(8, len(drawings))

    def test_list_application_drawings(self):
        """Can list the drawings associated with a patent application?
        """
        drawings = crud.list_drawings(self.app)
        self.assertEqual(8, len(drawings))

    def test_get_patent_drawing(self):
        """Can retrieve a given patent's drawing?
        """
        tif_data = crud.get_drawing(self.pn, 1)
        self.assertEqual(43060, len(tif_data))

    def test_get_application_drawing(self):
        """Can retrieve a given patent application's drawing?
        """
        tif_data = crud.get_drawing(self.app, 1)
        self.assertEqual(78716, len(tif_data))

    def test_delete_patent(self):
        """Can it delete a patent application, given its patent number
        """
        key = 'US7654321A2'
        data = {"test_key": "test_value"}
        # crud.put_doc(key, data) is required to test
        pass 




class TestOperations_Local(unittest.TestCase):

    """Test CRUD operations for 
    """

    def setUp(self):
        """Initialize example patent and application numbers

        Separate tests are written for patents and applications because their
        data is published differently by the patent offices and consequently,
        processed and stored differently.
        """
        self.pn = 'US7654321B2'
        self.app = 'US20080156487A1'
        os.environ["STORAGE"] = 'local'
        
    def test_get_patent(self):
        """Can retrieve a patent by its patent number?
        """
        patent = crud.get_doc(self.pn)
        self.assertIsInstance(patent, dict)
        self.assertEqual(self.pn, patent['publicationNumber'])
        self.assertIn('title', patent)
        self.assertIn('abstract', patent)
        self.assertIn('publicationDate', patent)

    def test_get_application(self):
        """Can retrieve a patent application given its publication number?
        """
        patent = crud.get_doc(self.app)
        self.assertIsInstance(patent, dict)
        self.assertEqual(self.app, patent['publicationNumber'])
        self.assertIn('title', patent)
        self.assertIn('abstract', patent)
        self.assertIn('publicationDate', patent)

    def test_list_patent_drawings(self):
        """Can list the drawings associated with a patent?
        """
        drawings = crud.list_drawings(self.pn)
        self.assertEqual(8, len(drawings))

    def test_list_application_drawings(self):
        """Can list the drawings associated with a patent application?
        """
        drawings = crud.list_drawings(self.app)
        self.assertEqual(8, len(drawings))

    def test_get_patent_drawing(self):
        """Can retrieve a given patent's drawing?
        """
        tif_data = crud.get_drawing(self.pn, 1)
        self.assertEqual(43060, len(tif_data))

    def test_get_application_drawing(self):
        """Can retrieve a given patent application's drawing?
        """
        tif_data = crud.get_drawing(self.app, 1)
        self.assertEqual(78716, len(tif_data))

    def test_delete_patent(self):
        """Can it delete a patent application, given its patent number
        """
        pn = 'US7654321A2'
        data = b'{"test_key": "test_value"}'
        pn_file = pn + '.json'
        path = str((TEST_DIR / 'test-dir/patents' / pn_file).resolve())
        with open(path, 'wb') as f:
            f.write(data)

        is_file = os.path.exists(path) #should exist
        self.assertTrue(is_file)
        crud.delete_doc(pn)
        is_file = os.path.exists(path) # shouldn't exist
        self.assertFalse(is_file)
        
if __name__ == '__main__':
    unittest.main()
