"""Contains utility methods for manipulating images."""
import cv2
import numpy as np


def get_resized_image(img_data: bytes, w: int, h: int):
    """Return a resized version of the given image.
    
    Args
    ----
    img_data: the data of a TIF image in bytecode format.
    w: the width the image should be resized to
    h: the height the image should be resized to

    Returns
    -------
    img_encode (bytes): the resized image in bytcode encoding
    """
    img = cv2.imdecode(np.asarray(bytearray(img_data)), 1)
    img = cv2.resize(img, (w, h), interpolation=cv2.INTER_AREA)
    img_encode = cv2.imencode('.tiff', img)[1]
    img_encode = np.array(img_encode)
    img_encode = img_encode.tobytes()
    return img_encode
