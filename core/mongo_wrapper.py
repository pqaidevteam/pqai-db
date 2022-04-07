"""
This is a custom wrapper around the PQAI MongoDB
"""

# Later pooling system can be used
# Bootstrapping the DB

import os
import dotenv
import pymongo

dotenv.load_dotenv()

MONGO_USERNAME = os.environ['MONGO_USERNAME']
MONGO_PASSWORD = os.environ['MONGO_PASSWORD']
MONGO_HOST = os.environ['MONGO_HOST']
MONGO_DB = 'pqai'
MONGO_COLL = 'docs'


class Mongo:

    """A wrapper class around the MongoDB to hide the it's retrieval details.
    """

    def __init__(self):
        uri = "mongodb://{}:{}@{}:27017/".format(MONGO_USERNAME, MONGO_PASSWORD, MONGO_HOST)
        client = pymongo.MongoClient(uri)
        self.coll = client[MONGO_DB][MONGO_COLL]

    def get(self, key):
        """Get an object from Mongo

        Args:
            key (str): Object's key

        Returns:
            dict: data of the object
        """
        doc_data = self.coll.find_one({"_id": key})
        if doc_data is None:
            raise Exception('Document not found in Mongo DB')
        return doc_data

    def put(self, key, data):
        """Add a new document to the Mongo database

        Args:
            key (str): Description
            data (dict): JSON data
        """
        data['_id'] = key
        self.coll.insert_one(data)

    def delete(self, key):
        """Remove an object from the mongo

        Args:
            key (str): Object's key
        """
        self.coll.delete_one({"_id": key})

    def list(self, key):
        """List the items matching the given key (used as a prefix)

        Return 1000 doc at once

        Args:
            key (str): mongo key prefix

        Returns:
            list: Matching data keys
        """
        query = {"_id": {"$regex": '{}.*'.format(key), "$options": 'i'}}
        return list(self.coll.find(query).limit(1000))
