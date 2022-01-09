import unittest, dotenv, os, sys, boto3
from pathlib import Path

TEST_DIR = Path(__file__).parent
BASE_DIR = Path(__file__).parent.parent
sys.path.append(str(BASE_DIR.resolve()))

dotenv.load_dotenv()

from core import crud

class TestOperations(unittest.TestCase):

    def setUp(self):
        self.pn = 'US7654321B2'
        self.app = 'US20080156487A1'

    def test_get_patent(self):
        patent = crud.get_doc(self.pn)
        self.assertIsInstance(patent, dict)
        self.assertEqual(self.pn, patent['publicationNumber'])
        self.assertIn('title', patent)
        self.assertIn('abstract', patent)
        self.assertIn('publicationDate', patent)

    def test_get_application(self):
        patent = crud.get_doc(self.app)
        self.assertIsInstance(patent, dict)
        self.assertEqual(self.app, patent['publicationNumber'])
        self.assertIn('title', patent)
        self.assertIn('abstract', patent)
        self.assertIn('publicationDate', patent)

    def test_list_patent_drawings(self):
        drawings = crud.list_drawings(self.pn)
        self.assertEqual(8, len(drawings))

    def test_list_application_drawings(self):
        drawings = crud.list_drawings(self.app)
        self.assertEqual(8, len(drawings))

    def test_get_patent_drawing(self):
        tif_data = crud.get_drawing(self.pn, 1)
        self.assertEqual(43060, len(tif_data))

    def test_get_application_drawing(self):
        tif_data = crud.get_drawing(self.app, 1)
        self.assertEqual(78716, len(tif_data))

if __name__ == '__main__':
    unittest.main()