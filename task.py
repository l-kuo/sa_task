import cv2
from PIL import Image
import numpy as np


def drawbb(img_file: bytes):

    x_topleft = 192
    y_topleft = 180
    width = 384 
    height = 75

    try:
        with open(img_file, 'rb') as fp:
            img_b = fp.read()
            
        img_np = np.frombuffer(img_b, np.uint8)
        img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
        h, w, c = img.shape

        if x_topleft < 0 or y_topleft < 0 or x_topleft+width > w or y_topleft+height > h:
            raise ValueError("The image size is not appropriate for the given bounding box.")

        cv2.rectangle(img, (x_topleft, y_topleft), (x_topleft+width, y_topleft+height), (0, 0, 255), 3)
        # cv2.imwrite("imgbb.png", img)
        # print(img)
        img = cv2.imencode('.jpg', img)[1].tobytes()
        return img
    except Exception as e:
        raise print(e)

img = drawbb('/home/kuo/Documents/fastapi/Ghost-Rider-Reading-Order.jpg')
print(img)