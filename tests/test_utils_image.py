from dotenv import load_dotenv
from pathlib import Path
import unittest
import sys
import cv2
import numpy as np

BASE_DIR = str(Path(__file__).parent.parent.resolve())
TEST_DIR = str(Path(__file__).parent.resolve())
sys.path.append(BASE_DIR)

load_dotenv(f"{BASE_DIR}/.env")

from core.storage import LocalStorage
from utils.image import get_resized_image


class TestImage(unittest.TestCase):
    def setUp(self):
        self.root = f"{TEST_DIR}/test-data"
        self.storage = LocalStorage(self.root)
        self.w = 100
        self.h = 100
    
    def test_get_resized_image(self):
        img_data = self.storage.get("images/sample.tiff")
        resized_image = get_resized_image(img_data, self.w, self.h)
        resized_image = cv2.imdecode(np.asarray(bytearray(resized_image)), 1)
        self.assertEqual(self.h, resized_image.shape[0])
        self.assertEqual(self.w, resized_image.shape[1])


if __name__ == '__main__':
    unittest.main()