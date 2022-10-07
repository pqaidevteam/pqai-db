import cv2
import numpy as np

img = cv2.imread('./image.tiff')
encoding = cv2.imencode('.tiff', img)

print(encoding)


img_encode = encoding[1]

print(img_encode)

data_encode = np.array(img_encode)
byte_encode = data_encode.tobytes()