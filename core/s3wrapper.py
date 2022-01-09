import os, json
import dotenv
import boto3
import botocore.exceptions

dotenv.load_dotenv()

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

botoclient = boto3.client('s3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

class S3Bucket:

    def __init__(self, bucket_name):
        self._bucket = bucket_name

    def get(self, key):
        obj = botoclient.get_object(Bucket=self._bucket, Key=key)
        contents = obj["Body"].read()
        return contents

    def put(self, key, data):
        botoclient.put_object(Body=data, Key=key, Bucket=self._bucket)

    def delete(self, key):
        botoclient.delete_object(Key=key, Bucket=self._bucket)

    def list(self, key):
        response = botoclient.list_objects(Bucket=self._bucket, Prefix=key)
        if not 'Contents' in response:
            return []
        items = response['Contents']
        return [item['Key'] for item in items]