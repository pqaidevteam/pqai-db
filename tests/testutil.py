
import os
import sys
import shutil
from pathlib import Path
import boto3
import dotenv

TEST_DIR = Path(__file__).parent
BASE_DIR = Path(__file__).parent.parent
sys.path.append(str(BASE_DIR.resolve()))

dotenv.load_dotenv()

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
TEST_BUCKET_NAME = 'pqai.test'

def get_botoclient():
    """Connect to S3
    """
    credentials = {
        'aws_access_key_id': AWS_ACCESS_KEY_ID,
        'aws_secret_access_key': AWS_SECRET_ACCESS_KEY
    }
    return boto3.client('s3', **credentials)

botoclient = get_botoclient()


class TestS3BucketCreator():

    def __init__(self):
        self._bucket_name = TEST_BUCKET_NAME
        self._files = [
            str((TEST_DIR / 'US7654321B2.json').resolve()),
            str((TEST_DIR / 'US20080156487A1.json').resolve())
        ]

    def create(self):
        if self._exists():
            self._erase()
        self._create_new()
        self._upload_test_files()
        return self._bucket_name

    def _exists(self):
        response = botoclient.list_buckets()
        buckets = [bucket['Name'] for bucket in response['Buckets']]
        return self._bucket_name in buckets

    def _erase(self):
        bucket = boto3.resource('s3').Bucket(self._bucket_name)
        for key in bucket.objects.all():
            key.delete()
        bucket.delete()

    def _create_new(self):
        botoclient.create_bucket(Bucket=self._bucket_name)

    def _upload_test_files(self):
        for path in self._files:
            with open(path, 'rb') as fp:
                data = fp.read()
            filename = path.split('/').pop()
            key = f'patents/{filename}'
            botoclient.put_object(Body=data, Key=key, Bucket=self._bucket_name)


def set_up_test_local_directory():
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

if __name__ == '__main__':
    TestS3BucketCreator().create()
