"""
Unit test for custom wrapper around S3 storage
"""

# pylint: disable=C0103,C0413

import unittest
import os
import sys
from pathlib import Path

import boto3
import dotenv

TEST_DIR = Path(__file__).parent
BASE_DIR = Path(__file__).parent.parent
sys.path.append(str(BASE_DIR.resolve()))

from core.s3wrapper import S3Bucket, get_botoclient

dotenv.load_dotenv()

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

botoclient = get_botoclient()

class TestS3BucketOperations(unittest.TestCase):

    """Test object uploading, downloading, and listing operations of an
        S3 bucket

    Attributes:
        test_bucket (S3Bucket): A disposable S3 bucket created for testing
        TEST_BUCKET_NAME (str): Name of the test bucket
        test_data (str): Data of the test object
        test_key (str): S3 key for storing the test object
    """

    TEST_BUCKET_NAME = 'pqai.test'

    def setUp(self):
        """Initial setup
        """
        self._reset_test_bucket()
        self.test_bucket = S3Bucket(self.TEST_BUCKET_NAME)
        self.test_key = 'patents/US7654321B2.json'
        local_file = str((TEST_DIR / 'US7654321B2.json').resolve())
        with open(local_file, 'r', encoding='UTF-8') as f:
            self.test_data = f.read()

    def _reset_test_bucket(self):
        """Delete (if needed) and (re)create a disposable test S3 bucket
        """
        if self._exists(self.TEST_BUCKET_NAME):
            self._erase_test_bucket()
        self._create_new_test_bucket()

    def _erase_test_bucket(self):
        """Delete the S3 test bucket
        """
        bucket = boto3.resource('s3').Bucket(self.TEST_BUCKET_NAME)
        for key in bucket.objects.all():
            key.delete()
        bucket.delete()

    def _create_new_test_bucket(self):
        """Create the test bucket

        Raises:
            Error: if the S3 bucket couldn't be created
        """
        botoclient.create_bucket(Bucket=self.TEST_BUCKET_NAME)
        if not self._exists(self.TEST_BUCKET_NAME):
            raise Exception('Could not create test S3 bucket')

    @staticmethod
    def _exists(bucket_name):
        """Check if the S3 bucket with this name exists

        Args:
            bucket_name (str): Bucket name

        Returns:
            bool: True if it exists, False otherwise
        """
        response = botoclient.list_buckets()
        buckets = [bucket['Name'] for bucket in response['Buckets']]
        return bucket_name in buckets

    def test_operations(self):
        """Test by putting in a test object into the S3 bucket and then
            retrieving it, then deleting it at the end
        """
        self.assertObjectCount(0)
        self.test_bucket.put(self.test_key, self.test_data)
        self.assertObjectCount(1)
        downloaded = self.test_bucket.get(self.test_key)
        self.assertEqual(downloaded, self.test_data)
        self.test_bucket.delete(self.test_key)
        self.assertObjectCount(0)

    def assertObjectCount(self, n_expected):
        """For custom assertion statement that makes sure the S3 bucket contains
            an expected number of items

        Args:
            n_expected (int): Expected count
        """
        keys = self.test_bucket.list(self.test_key)
        self.assertEqual(n_expected, len(keys))

if __name__ == '__main__':
    unittest.main()
