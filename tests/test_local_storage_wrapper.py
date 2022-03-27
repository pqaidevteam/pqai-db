"""
Unit test for custom wrapper around local storage
"""
import unittest
import os
import sys
import json
import shutil
from pathlib import Path

TEST_DIR = Path(__file__).parent
BASE_DIR = Path(__file__).parent.resolve().parent
sys.path.append(str(BASE_DIR))

from core.local_storage_wrapper import LocalStorage

class TestLocalStorage(unittest.TestCase):
    
    """Testing getting, putting, deleting and listing operations of a test file

    Attributes:
        test_dir (str): Directory in which all the test will be done
        test_subdir (str): A sub directory under the test_dir where similar files
                           will be stored together 
        test_file (str): file where tests will be done
    """

    def setUp(self):
        """Initial setup
        """
        self.test_dir = str((TEST_DIR / 'test-dir').resolve())
        self.test_subdir = str((TEST_DIR / 'test-dir/patents').resolve())
        self.test_file = str((TEST_DIR / 'test-dir/patents/US7654321B2.json').resolve())
        if os.path.exists(self.test_subdir):
            shutil.rmtree(self.test_subdir)
        os.mkdir(self.test_subdir)
        with open(self.test_file, 'w') as f:
            f.write(json.dumps({'publicationNumber': 'US7654321B2'}))

    def test_initialize(self):
        """Test whether LocalStorage Class can create a instance or not
        """
        local_storage = LocalStorage(self.test_dir)
        self.assertIsInstance(local_storage, LocalStorage)

    def test_get_file(self):
        """Test by retrieving the contents of a file and verify it.
        """
        local_storage = LocalStorage(self.test_dir)
        rel_path = 'patents/US7654321B2.json'
        contents = local_storage.get(rel_path)
        self.assertIsInstance(contents, bytes)
        self.assertGreater(len(contents), 0)
    
    def test_error_when_reading_non_existing_file(self):
        """Test by retrieving an non existing file and check whether
        error is raised or not
        """
        local_storage = LocalStorage(self.test_dir)
        rel_path = 'patents/not_exist.json'
        attempt = lambda: local_storage.get(rel_path)
        self.assertRaises(FileNotFoundError, attempt)
    
    def test_put_file(self):
        """Test by putting data into a new file and reading and verifying
        the contents and deleting it in the end
        """
        local_storage = LocalStorage(self.test_dir)
        rel_path = 'patents/new.json'
        data = b'{"test_key": "test_value"}'
        path = Path(self.test_dir + rel_path)
        if path.is_file():
            local_storage.delete(rel_path)
        local_storage.put(rel_path, data)    
        downloaded = local_storage.get(rel_path)
        self.assertEqual(downloaded, data)
        local_storage.delete(rel_path)

    def test_delete_file(self):
        """Test by creating a new file then deleting it and checking the
        validity its path, also checking whether error is raised when non
        existing file is deleted.
        """
        local_storage = LocalStorage(self.test_dir)
        rel_path = 'patents/test.json'
        data = b'{ "test_key": "test_value"}'
        contents = local_storage.put(rel_path, data)
        local_storage.delete(rel_path)
        path = Path(self.test_dir + rel_path)
        self.assertFalse(path.is_file())

        rel_path = 'patent/not_exist.json'
        attempt = lambda: local_storage.delete(rel_path)
        self.assertRaises(FileNotFoundError, attempt)
    
    def test_list_files(self):
        """Test by checking whether a list returned and also the expected no. of 
        files are retireved given a valid/invalid key
        """
        local_storage = LocalStorage(self.test_dir) # prefix
        key = 'patents/US'
        output = local_storage.list(key)
        self.assertIs(type(output), list)
        self.assertGreater(len(output), 0)

        key = 'patents/notexist'
        output = local_storage.list(key)
        self.assertEqual(len(output), 0)
        

if __name__ == "__main__":
    unittest.main()

