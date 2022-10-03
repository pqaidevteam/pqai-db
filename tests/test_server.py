import unittest
import sys
from pathlib import Path
from fastapi.testclient import TestClient
import dotenv

BASE_DIR = Path(__file__).parent.parent.resolve()
ENV_PATH = BASE_DIR / ".env"

sys.path.append(BASE_DIR.as_posix())
dotenv.load_dotenv(ENV_PATH.as_posix())

from main import app


class TestServer(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test__document_route(self):
        res = self.client.get("/patents/US7654321B2")
        self.assertEqual(200, res.status_code)
        patent = res.json()
        self.assertIsInstance(patent, dict)
        self.assertEqual("US7654321B2", patent["publicationNumber"])
    
    def test__document_route__not_found(self):
        pn_ = "US987654321B3" # invalid patent number
        res = self.client.get(f"/patents/{pn_}")
        self.assertEqual(404, res.status_code)

    def test__drawing_listing_route(self):
        res = self.client.get("/patents/US7654321B2/drawings")
        self.assertEqual(200, res.status_code)
        drawings = res.json().get("drawings")
        self.assertIsInstance(drawings, list)
        self.assertEqual(8, len(drawings))
    
    def test__drawing_listing_route__patent_not_found(self):
        pn_ = "US987654321B3"  # invalid patent number
        res = self.client.get(f"/patents/{pn_}/drawings")
        self.assertEqual(404, res.status_code)
    
    def test__drawing_listing_route__patent_without_drawings(self):
        pn = "US8507721B2"
        res = self.client.get(f"/patents/{pn}/drawings")
        self.assertEqual(404, res.status_code)

    def test__drawing_route(self):
        res = self.client.get("/patents/US7654321B2/drawings/1")
        self.assertEqual(200, res.status_code)
        self.assertEqual("image/tiff", res.headers["Content-Type"])
        self.assertEqual(43060, len(res.content))
    
    def test__drawing_route__invalid_drawing_number(self):
        res = self.client.get("/patents/US7654321B2/drawings/0")
        self.assertEqual(404, res.status_code)
    
    def test__drawing_route__non_existent_patents_drawing(self):
        pn_ = "US987654321B3"  # invalid patent number
        res = self.client.get(f"/patents/{pn_}/drawings/1")
        self.assertEqual(404, res.status_code)


if __name__ == "__main__":
    unittest.main()
