"""
This is a custom wrapper around the PQAI S3 bucket
"""

import os
import boto3

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

def get_botoclient():
    """Connect to S3
    """
    credentials = {
        'aws_access_key_id': AWS_ACCESS_KEY_ID,
        'aws_secret_access_key': AWS_SECRET_ACCESS_KEY
    }
    return boto3.client('s3', **credentials)

BOTO_CLIENT = get_botoclient()

class S3Bucket:

    """A wrapper class around an S3 bucket to hide the S3 retrieval details.
    """

    def __init__(self, bucket_name):
        """Creates an S3Bucket class

        Args:
            bucket_name (str): S3 bucket identifier
        """
        self._bucket = bucket_name

    def get(self, key):
        """Get the raw binary data of an object from S3

        Args:
            key (str): Object's key

        Returns:
            bytes: Raw data of the object
        """
        obj = BOTO_CLIENT.get_object(Bucket=self._bucket, Key=key)
        contents = obj["Body"].read()
        return contents

    def put(self, key, data):
        """Put a new object into the S3 bucket

        Args:
            key (str): Description
            data (bytes): Raw data of the object
        """
        BOTO_CLIENT.put_object(Body=data, Key=key, Bucket=self._bucket)

    def delete(self, key):
        """Remove an object from the S3 bucket

        Args:
            key (str): Object's key
        """
        BOTO_CLIENT.delete_object(Key=key, Bucket=self._bucket)

    def list(self, key):
        """List the items matching the given key (used as a prefix)

        Only first 1000 matches are returned.

        Args:
            key (str): S3 object key prefix

        Returns:
            list: Matching object keys
        """
        response = BOTO_CLIENT.list_objects(Bucket=self._bucket, Prefix=key)
        if not 'Contents' in response:
            return []
        items = response['Contents']
        return [item['Key'] for item in items]
