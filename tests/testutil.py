"""Test utilities
"""
import os
import shutil
from pathlib import Path
import boto3
import dotenv

TEST_DIR = Path(__file__).parent
BASE_DIR = Path(__file__).parent.parent

def load_test_environment():
    """Set environment variables for testing
    """
    test_env_file = str((BASE_DIR / '.env.test').resolve())
    dotenv.load_dotenv(test_env_file)


class TestS3BucketCreator():

    """Creates an S3 bucket used for testing
    """

    def __init__(self):
        """Initialize
        """
        self._bucket_name = os.environ['AWS_S3_BUCKET_NAME']
        self._files = [
            str((TEST_DIR / 'US7654321B2.json').resolve()),
            str((TEST_DIR / 'US20080156487A1.json').resolve())
        ]
        credentials = {
            'aws_access_key_id': os.environ['AWS_ACCESS_KEY_ID'],
            'aws_secret_access_key': os.environ['AWS_SECRET_ACCESS_KEY']
        }
        self.botoclient = boto3.client('s3', **credentials)

    def create(self):
        """Create a fresh test bucket (if needed, delete pre-existing)

        Returns:
            str: Test bucket name
        """
        if self.exists():
            self._erase()
        self._create_new()
        self._upload_test_files()
        return self._bucket_name

    def exists(self):
        """Check if test bucket pre-exists

        Returns:
            bool: True if test bucket exists, False otherwise
        """
        response = self.botoclient.list_buckets()
        buckets = [bucket['Name'] for bucket in response['Buckets']]
        return self._bucket_name in buckets

    def _erase(self):
        """Remove a pre-existing S3 bucket (along with its contents)
        """
        bucket = boto3.resource('s3').Bucket(self._bucket_name)
        for key in bucket.objects.all():
            key.delete()
        bucket.delete()

    def _create_new(self):
        """Create a new test bucket
        """
        self.botoclient.create_bucket(Bucket=self._bucket_name)

    def _upload_test_files(self):
        """Update test files to newly created S3 bucket
        """
        for path in self._files:
            with open(path, 'rb') as fp:
                data = fp.read()
            filename = path.split('/').pop()
            key = f'patents/{filename}'
            self.botoclient.put_object(Body=data, Key=key, Bucket=self._bucket_name)


def set_up_test_local_directory():
    """Initialize test data directory

    Returns:
        str: Absolute local path of test data directory
    """
    test_data_dir = str((TEST_DIR / 'test-data').resolve())
    if not os.path.exists(test_data_dir):
        os.mkdir(test_data_dir)

    test_patents_dir = str((TEST_DIR / 'test-data/patents').resolve())
    if not os.path.exists(test_patents_dir):
        os.mkdir(test_patents_dir)

    for item in os.scandir(test_patents_dir):
        if os.path.isfile(item.path):
            os.remove(item.path)

    src = str((TEST_DIR / 'US7654321B2.json').resolve())
    dst = str((TEST_DIR / 'test-data/patents/US7654321B2.json').resolve())
    shutil.copyfile(src, dst)

    return test_data_dir
