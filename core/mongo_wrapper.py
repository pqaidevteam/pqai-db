"""
This is a custom wrapper around the PQAI MongoDB
"""

# Later pooling system can be used
# Bootstrapping the DB 

import os
import dotenv
import boto3
import pymongo
import json

dotenv.load_dotenv()

MONGO_USERNAME = os.environ['MONGO_USERNAME']
MONGO_PASSWORD = os.environ['MONGO_PASSWORD']
MONGO_URL = os.environ['MONGO_URL']


def getMongoClient():
    """Connect to Mongo
    """

    uri = "mongodb://{}:{}@{}:27017/".format(MONGO_USERNAME, MONGO_PASSWORD, MONGO_URL)

    client = pymongo.MongoClient(uri)
    db = client["pqai"]
    collection = db["docs"]

    return collection

collection = getMongoClient()

class Mongo:

    """A wrapper class around the MongoDB to hide the it's retrieval details.
    """

    def __init__(self):
        """Creates a Mongo class
        """
        pass

    def get(self, key):
        """Get the raw binary data of an object from Mongo

        Args:
            key (str): Object's key

        Returns:
            JSON: data of the object
        """
        doc_data = collection.find_one({"_id": key})
        return doc_data

    def put(self, data):
        """Put a new object into the S3 bucket

        Args:
            key (str): Description
            data (bytes): JSON object
        """
        collection.insert_one(data)

    def delete(self, key):
        """Remove an object from the mongo

        Args:
            key (str): Object's key
        """
        collection.delete_one({"_id": key})

    def list(self, key):
        """List the items matching the given key (used as a prefix)

        Return 1000 doc at once

        Args:
            key (str): mongo key prefix

        Returns:
            list: Matching data keys
        """
        return list(collection.find({ "_id": { "$regex": '{}.*'.format(key), "$options": 'i' } }).limit(1000))
