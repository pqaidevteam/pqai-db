"""
The purpose of this module is to hide the actual mechanism used for storing
document data from its user.

For example, the storage can be local (e.g. in a file system or database) or
in a remote location (e.g. and API or cloud storage). There can be single
storage or multiple storages (e.g. separate for text and image data, etc.)
"""

import os
import json
import re
from core.s3wrapper import S3Bucket
from core.local_storage_wrapper import LocalStorage
from core.mongo_wrapper import Mongo


S3_BUCKET = S3Bucket(os.environ['AWS_S3_BUCKET_NAME'])
S3_BUCKET_DRAWINGS = S3Bucket(os.environ['S3_BUCKET_DRAWINGS'])
LOCAL_STORAGE = LocalStorage(os.environ['LOCAL_STORAGE_ROOT'])
STORAGE = os.environ['STORAGE']
MONGO = Mongo()



def get_doc(doc_id):
    """Get a document data given document identifier (e.g. patent number)

    Args:
        doc_id (str): Document identifier (e.g. patent number)

    Returns:
        dict: Document data
    """

    match STORAGE :
        case "mongo":
            return MONGO.get(doc_id)
        case "local":
            key = f'patents/{doc_id}.json'
            contents = LOCAL_STORAGE.get(key).decode()
            return json.loads(contents)
        case "s3":
            key = f'patents/{doc_id}.json'
            contents = S3_BUCKET.get(key).decode()
            return json.loads(contents)
        case _: #default
            pass

def delete_doc(doc_id):
    """Delete a document

    Args:
        doc_id (str): Document identifier (e.g. patent number)

    Returns:
       None
    """

    match STORAGE:
        case "mongo":
            MONGO.delete(doc_id)
        case "local":
            key = f'patents/{doc_id}.json'
            LOCAL_STORAGE.delete(key)
        case "s3":
            key = f'patents/{doc_id}.json'
            S3_BUCKET.delete(key)
        case _: # default
            pass

def list_drawings(doc_id):
    """Summary

    Args:
        doc_id (str): Document identifier (e.g. patent number)

    Returns:
        list: Drawing identifiers, e.g. ["1", "2", "3"]
    """
    key_prefix = _drawing_prefix(doc_id)
    keys = S3_BUCKET_DRAWINGS.list(key_prefix)
    drawings = [re.search(r'-(\d+)', key).group(1) for key in keys]
    return drawings

def get_drawing(doc_id, drawing_num):
    """Summary

    Args:
        doc_id (str): Document identifier (e.g. patent number)
        drawing_num (str): Drawing number, e.g. "1"

    Returns:
        bytes: Image data
    """
    key_prefix = _drawing_prefix(doc_id)
    key = f'{key_prefix}{drawing_num}.tif'
    tif_data = S3_BUCKET_DRAWINGS.get(key)
    return tif_data

def _drawing_prefix(doc_id):
    """Maps document ids to their drawing path prefixes

    For US Patent No. 7,654,321 the drawings are stored as follows:
        07654321-1.tif
        07654321-2.tif
        ...
        ...
    For US patent applications, say, for US20080156487A1, they're stored as:
        US20080156487A1-1.tif
        US20080156487A1-2.tif
        ...
        ...
    This function creates the appropriate key prefix on the basis of whether
    the supplied number is a patent or an application.

    Args:
        doc_id (str): Document identifier (e.g. patent number)

    Returns:
        str: Drawing prefix
    """
    if len(doc_id) > 12:
        return f'images/{doc_id}-'

    num = re.search(r'\d+', doc_id).group(0)
    while len(num) < 8:
        num = '0' + num
    return f'images/{num}-'
