from dotenv import load_dotenv
from pathlib import Path
import unittest
import sys

BASE_DIR = str(Path(__file__).parent.parent.resolve())
TEST_DIR = str(Path(__file__).parent.resolve())
sys.path.append(BASE_DIR)

load_dotenv(f"{BASE_DIR}/.env")

from core.storage import LocalStorage
from utils.data import get_storage_from_config


class TestData(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_get_local_storage(self):
        storage = get_storage_from_config('localstorage')
        self.assertTrue(isinstance(storage, LocalStorage))


if __name__ == '__main__':
    unittest.main()