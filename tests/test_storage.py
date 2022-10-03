import unittest
import sys
import os
import json
from pathlib import Path
from dotenv import load_dotenv
import boto3
import botocore
from pymongo import MongoClient

BASE_DIR = str(Path(__file__).parent.parent.resolve())
TEST_DIR = str(Path(__file__).parent.resolve())
sys.path.append(BASE_DIR)

load_dotenv(f"{BASE_DIR}/.env")

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
MONGO_HOST = os.environ.get("MONGO_HOST")
MONGO_PORT = os.environ.get("MONGO_PORT")
MONGO_USER = os.environ.get("MONGO_USER")
MONGO_PASS = os.environ.get("MONGO_PASS")
MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}"

from core.storage import LocalStorage, S3Bucket, MongoDB


class TestLocalStorage(unittest.TestCase):
    def setUp(self):
        self.root = f"{TEST_DIR}/test-data"
        self.storage = LocalStorage(self.root)

    def test__can_fetch_item(self):
        item = self.storage.get("patents/US7654321B2.json")
        self.assertIsInstance(item, bytes)

    def test__can_list_items(self):
        item = self.storage.ls("patents")
        self.assertEqual(1, len(item))

    def test__can_check_if_item_exists(self):
        exists = self.storage.exists("patents/US7654321B2.json")
        self.assertTrue(exists)
        exists = self.storage.exists("patents/non-existent.json")
        self.assertFalse(exists)

    def test__can_store_and_remove_items(self):
        key = "patents/test.json"
        path = f"{self.root}/{key}"
        if os.path.exists(path):
            os.remove(path)

        data = bytes(json.dumps({"key": "value"}), "utf-8")
        self.storage.put(key, data)
        self.assertTrue(os.path.exists(path))
        self.assertTrue(self.storage.exists(key))

        self.storage.remove(key)
        self.assertFalse(os.path.exists(path))
        self.assertFalse(self.storage.exists(key))


class TestS3Bucket(unittest.TestCase):
    def setUp(self):
        config = botocore.config.Config(
            read_timeout=400, connect_timeout=400, retries={"max_attempts": 0}
        )
        credentials = {
            "aws_access_key_id": AWS_ACCESS_KEY_ID,
            "aws_secret_access_key": AWS_SECRET_ACCESS_KEY,
        }
        botoclient = boto3.client("s3", **credentials, config=config)
        bucket_name = "pqai.test1"
        self.storage = S3Bucket(botoclient, bucket_name)

    def test__can_fetch_item(self):
        item = self.storage.get("patents/US7654321B2.json")
        self.assertIsInstance(item, bytes)

    def test__can_list_items(self):
        items = self.storage.ls("patents/US7654321B2.json")
        self.assertGreater(len(items), 0)

    def test__can_check_if_item_exists(self):
        exists = self.storage.exists("patents/US7654321B2.json")
        self.assertTrue(exists)
        exists = self.storage.exists("patents/nonexistent.json")
        self.assertFalse(exists)

    def test__can_store_and_remove_items(self):
        key = "patents/test.json"
        if self.storage.exists(key):
            self.storage.remove(key)
        self.assertFalse(self.storage.exists(key))

        data = bytes(json.dumps({"key": "value"}), "utf-8")
        self.storage.put(key, data)
        self.assertTrue(self.storage.exists(key))

        self.storage.remove(key)
        self.assertFalse(self.storage.exists(key))


class TestMongoDB(unittest.TestCase):
    def setUp(self):
        client = MongoClient(MONGO_URI)
        collections = [coll["name"] for coll in client.gamma.list_collections()]
        if "test" in collections:
            client.gamma.test.drop()
        with open(f"{TEST_DIR}/test-data/patents/US7654321B2.json", "r") as f:
            data = json.load(f)
            client.gamma.test.insert_one(data)
        self.storage = MongoDB(client, "gamma", "test", "publicationNumber")

    def test__can_fetch_item(self):
        item = self.storage.get("US7654321B2")
        self.assertIsInstance(item, bytes)

    def test__can_list_items(self):
        items = self.storage.ls("US7654321B2")
        self.assertGreater(len(items), 0)

    def test__can_check_if_item_exists(self):
        exists = self.storage.exists("US7654321B2")
        self.assertTrue(exists)
        exists = self.storage.exists("nonexistent")
        self.assertFalse(exists)

    def test__can_store_and_remove_items(self):
        key = "test"
        if self.storage.exists(key):
            self.storage.remove(key)
        self.assertFalse(self.storage.exists(key))

        data = bytes(json.dumps({"publicationNumber": "US3344334A"}), "utf-8")
        self.storage.put(key, data)
        self.assertTrue(self.storage.exists(key))

        self.storage.remove(key)
        self.assertFalse(self.storage.exists(key))


if __name__ == "__main__":
    unittest.main()
