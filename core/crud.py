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
from pathlib import Path

import dotenv
from core.s3wrapper import S3Bucket
from core.local_storage_wrapper import LocalStorage

dotenv.load_dotenv()

AWS_S3_BUCKET_NAME = os.environ['AWS_S3_BUCKET_NAME']
s3_bucket = S3Bucket(AWS_S3_BUCKET_NAME)
storage = os.environ['STORAGE']

BASE_DIR = Path(__file__).parent.parent
FILE_DIR = str((BASE_DIR / 'tests/test-dir').resolve())
local_storage = LocalStorage(FILE_DIR)

def get_doc(doc_id):
    """Get a document data gives document identifier (e.g. patent number)

    Args:
        doc_id (str): Document identifier (e.g. patent number)

    Returns:
        dict: Document data
    """
    key = f'patents/{doc_id}.json'
    contents = s3_bucket.get(key).decode()
    return json.loads(contents)

def delete_doc(doc_id):
    """Delete the document with the given document identifier

    Args:
        doc_id (str): Document identifier (e.g. patent number)

    Returns:
       None
    """
    key = f'patents/{doc_id}.json'
    if storage == "local":
        local_storage.delete(key)
    
    else:
        pass
        #s3_bucket.delete(key) untested

def list_drawings(doc_id):
    """Summary

    Args:
        doc_id (str): Document identifier (e.g. patent number)

    Returns:
        list: Drawing identifiers, e.g. ["1", "2", "3"]
    """
    key_prefix = _drawing_prefix(doc_id)
    keys = s3_bucket.list(key_prefix)
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
    tif_data = s3_bucket.get(key)
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
