import unittest, dotenv, os, sys, boto3
from pathlib import Path

TEST_DIR = Path(__file__).parent
BASE_DIR = Path(__file__).parent.parent
sys.path.append(str(BASE_DIR.resolve()))

dotenv.load_dotenv()

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

botoclient = boto3.client('s3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

from s3 import S3Bucket


class TestS3BucketOperations(unittest.TestCase):

    TEST_BUCKET_NAME = 'pqai.test'

    def setUp(self):
        self._reset_test_bucket()
        self.test_bucket = S3Bucket(self.TEST_BUCKET_NAME)
        self.test_key = 'patents/US7654321B2.json'
        local_file = str((TEST_DIR / 'US7654321B2.json').resolve())
        with open(local_file, 'r') as f:
            self.test_data = f.read()

    def _reset_test_bucket(self):
        if self._exists(self.TEST_BUCKET_NAME):
            self._erase_test_bucket()
        self._create_new_test_bucket()

    def _erase_test_bucket(self):
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(self.TEST_BUCKET_NAME)
        for key in bucket.objects.all():
            key.delete()
        bucket.delete()

    def _create_new_test_bucket(self):
        botoclient.create_bucket(Bucket=self.TEST_BUCKET_NAME)
        if not self._exists(self.TEST_BUCKET_NAME):
            raise Error('Could not create test S3 bucket')

    def _exists(self, bucket_name):
        response = botoclient.list_buckets()
        buckets = [bucket['Name'] for bucket in response['Buckets']]
        return bucket_name in buckets

    def test_operations(self):
        self.assertObjectCount(0)
        self.test_bucket.put(self.test_key, self.test_data)
        self.assertObjectCount(1)
        downloaded = self.test_bucket.get(self.test_key)
        self.assertEqual(downloaded, self.test_data)
        self.test_bucket.delete(self.test_key)
        self.assertObjectCount(0)

    def assertObjectCount(self, n):
        keys = self.test_bucket.list(self.test_key)
        self.assertEqual(n, len(keys))

if __name__ == '__main__':
    unittest.main()