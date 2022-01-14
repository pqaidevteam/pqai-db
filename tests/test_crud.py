"""Unit tests for the `crud` module

Attributes:
    BASE_DIR (TYPE): Description
    TEST_DIR (TYPE): Description
"""

# pylint: disable=C0103

import unittest
import sys
from pathlib import Path

import dotenv
from core import crud

TEST_DIR = Path(__file__).parent
BASE_DIR = Path(__file__).parent.parent
sys.path.append(str(BASE_DIR.resolve()))

dotenv.load_dotenv()

class TestOperations(unittest.TestCase):

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

if __name__ == '__main__':
    unittest.main()
