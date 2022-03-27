"""
The purpose of this module is to hide the actual mechanism used for storing
document data in the local storage, from its user.
"""
import os
import sys
import json
from pathlib import Path

from core.local_storage_wrapper import LocalStorage

BASE_DIR = Path(__file__).parent.parent
sys.path.append(str(BASE_DIR.resolve()))

file_dir = str((BASE_DIR / 'tests/test-dir').resolve())
local_storage = LocalStorage(file_dir)

def get_doc(doc_id):
    pass

def delete_doc(doc_id):
    key = f'patents/{doc_id}.json'
    local_storage.delete(key)

def list_drawings(doc_id):
    pass

def get_drawing(doc_id, drawing_num):
    pass

def _drawing_prefix(doc_id):
    pass
