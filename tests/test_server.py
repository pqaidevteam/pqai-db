import unittest
import os
import socket
import requests
from pathlib import Path
import dotenv

BASE_DIR = str(Path(__file__).parent.parent.resolve())
dotenv.load_dotenv(f"{BASE_DIR}/.env")

PROTOCOL = 'http'
HOST = '127.0.0.1'
PORT = int(os.environ['PORT'])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_not_running = sock.connect_ex((HOST, PORT)) != 0
if server_not_running:
    print('Server is not running. All API tests will be skipped.')

@unittest.skipIf(server_not_running, 'Works only when true')
class TestServer(unittest.TestCase):

    def test__document_route(self):
        response = self.call_route('/patents/US7654321B2')
        self.assertEqual(200, response.status_code)
        patent = response.json()
        self.assertIsInstance(patent, dict)
        self.assertEqual('US7654321B2', patent['publicationNumber'])

    def test__drawing_listing_route(self):
        response = self.call_route('/patents/US7654321B2/drawings')
        self.assertEqual(200, response.status_code)
        drawings = response.json()
        self.assertIsInstance(drawings, list)
        self.assertEqual(8, len(drawings))

    def test__drawing_route(self):
        response = self.call_route('/patents/US7654321B2/drawings/1')
        self.assertEqual(200, response.status_code)

    @staticmethod
    def call_route(route, method='get'):
        """Make a GET request to a specific route
        """
        url = f'{PROTOCOL}://{HOST}:{PORT}' + route
        response = getattr(requests, method)(url)
        return response

if __name__ == '__main__':
    unittest.main()
