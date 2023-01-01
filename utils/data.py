"""Contains helper methods to initialize Storage instances for patent, bibliography and drawing data."""
from botocore.exceptions import ClientError
from pymongo import MongoClient
import boto3
import botocore
import os
import dotenv

dotenv.load_dotenv()

from core.storage import S3Bucket, LocalStorage, MongoDB


# AWS configurations
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
s3_config = botocore.config.Config(
    read_timeout=400, connect_timeout=400, retries={"max_attempts": 0}
)
credentials = {
    "aws_access_key_id": AWS_ACCESS_KEY_ID,
    "aws_secret_access_key": AWS_SECRET_ACCESS_KEY,
}
botoclient = boto3.client("s3", **credentials, config=s3_config)
bucket_name = os.environ.get("AWS_S3_BUCKET_NAME")


# Mongo DB configurations
LOCAL_STORAGE_ROOT = os.environ.get('LOCAL_STORAGE_ROOT')


# Localstorage configurations
MONGO_HOST = os.environ.get('MONGO_HOST')
MONGO_PORT = os.environ.get('MONGO_PORT')
MONGO_USER = os.environ.get('MONGO_USER')
MONGO_PASS = os.environ.get('MONGO_PASS')
MONGO_DB = os.environ.get('MONGO_DB')
MONGO_COLL = os.environ.get('MONGO_COLL')


def get_storage_from_config(storage_source: str, **kwargs):
    """Initialize and return the appropriate Storage instance based on the given source."""
    if storage_source == "s3":
        storage = S3Bucket(botoclient, bucket_name)
    elif storage_source == "mongodb":
        url = f"mongodb://{MONGO_USER}:{MONGO_PASS}.{MONGO_HOST}:{MONGO_PORT}"
        client = MongoClient(url)
        storage = MongoDB(client, MONGO_DB, MONGO_COLL, kwargs.get('field'))
    else:
        storage = LocalStorage(LOCAL_STORAGE_ROOT)
    return storage
