"""
Test all server routes
"""
import unittest
import os
import socket
import requests
import testutil

testutil.load_test_environment()

PROTOCOL = 'http'
HOST = '127.0.0.1'
PORT = int(os.environ['PORT'])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_not_running = sock.connect_ex((HOST, PORT)) != 0
if server_not_running:
    print('Server is not running. All API tests will be skipped.')

@unittest.skipIf(server_not_running, 'Works only when true')
class TestServer(unittest.TestCase):

    """Test the REST API routes
    """

    def test_document_route(self):
        """Can retrieve a document's data
        """
        response = self.call_route('/docs/US7654321B2')
        self.assertEqual(200, response.status_code)
        patent = response.json()
        self.assertIsInstance(patent, dict)
        self.assertEqual('US7654321B2', patent['publicationNumber'])

    def test_drawing_listing_route(self):
        """Can retrieve a list of drawings associated with a document
        """
        response = self.call_route('/docs/US7654321B2/drawings')
        self.assertEqual(200, response.status_code)
        drawings = response.json()
        self.assertIsInstance(drawings, list)
        self.assertEqual(8, len(drawings))

    def test_drawing_route(self):
        """Can obtain a drawing
        """
        response = self.call_route('/docs/US7654321B2/drawings/1')
        self.assertEqual(200, response.status_code)

    def test_delete_route(self):
        """ Can Delete File
        """
        pn = 'US7654321A2'
        route = f'/docs/{pn}'

        response = self.call_route(route, 'delete')
        self.assertEqual(200, response.status_code)

        response = self.call_route(route, 'delete')
        self.assertEqual(404, response.status_code)

    @staticmethod
    def call_route(route, method='get'):
        """Make a GET request to a specific route

        Args:
            route (str): Target route

        Returns:
            Response: Response object from `requests` module
        """

        url = f'{PROTOCOL}://{HOST}:{PORT}' + route
        response = getattr(requests, method)(url)
        return response

if __name__ == '__main__':
    unittest.main()
