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

    uri = "mongodb://{}:{}@{}:27017/".format(MONGO_USERNAME, MONGO_PASSWORD, MONGO_URL )

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
        """Get the raw binary data of an object from S3

        Args:
            key (str): Object's key

        Returns:
            json: data of the object
        """
        doc_data = collection.find_one({"_id":key})
        return doc_data

    def put(self, data):
        """Put a new object into the S3 bucket

        Args:
            key (str): Description
            data (bytes): Raw data of the object
        """
        obj = collection.insert_one(data)

    def delete(self, key):
        """Remove an object from the mongo

        Args:
            key (str): Object's key
        """
        collection.delete_one({"_id":key})

    def list(self, key):
        """List the items matching the given key (used as a prefix)

        Args:
            key (str): mongo key prefix

        Returns:
            list: Matching data keys
        """
        return list(collection.find({ "_id": { "$regex": 'US.*'.format(key), "$options" :'i' } }))


if __name__ == '__main__':
    # mongo = Mongo()
    
    # # Get doc data
    # print(mongo.get("US7654321B2"))
    
    # # Put doc Data
    # f = open("demo.json", "r") # create a file with this name and put json inside it
    # doc_data = f.read()
    # doc_data = json.loads(doc_data)
    # print(mongo.put(doc_data))
    
    # # Delete doc data
    # mongo.delete("US7654321B2")
    
    # # List doc matching the key
    # print(mongo.list("US"))

    pass