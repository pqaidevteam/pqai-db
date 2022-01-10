import requests
import unittest
import sys, os
import dotenv

from pathlib import Path

TEST_DIR = Path(__file__).parent
BASE_DIR = Path(__file__).parent.parent
sys.path.append(str(BASE_DIR.resolve()))

dotenv.load_dotenv()

PROTOCOL = 'http'
HOST = '127.0.0.1'
PORT = os.environ['PORT']


class TestServer(unittest.TestCase):

    def test_document_route(self):
        response = self.call_route('/docs/US7654321B2')
        self.assertEqual(200, response.status_code)
        patent = response.json()
        self.assertIsInstance(patent, dict)
        self.assertEqual('US7654321B2', patent['publicationNumber'])

    def test_drawing_listing_route(self):
        response = self.call_route('/docs/US7654321B2/drawings')
        self.assertEqual(200, response.status_code)
        drawings = response.json()
        self.assertIsInstance(drawings, list)
        self.assertEqual(8, len(drawings))

    def test_drawing_route(self):
        response = self.call_route('/docs/US7654321B2/drawings/1')
        self.assertEqual(200, response.status_code)

    def test_thumbnail_route(self):
        response = self.call_route('/docs/US7654321B2/thumbnails/1')
        self.assertEqual(200, response.status_code)

    def call_route(self, route):
        url = f'{PROTOCOL}://{HOST}:{PORT}' + route
        response = requests.get(url)
        return response


if __name__ == '__main__':
    unittest.main()