import numpy as np
import cv2 as cv
import base64

from io import BufferedReader, BytesIO

# 根据原图片的不同格式 贴上标签后 统一以base64编码

def stick_label_on_bytes(file, label_name):
    if isinstance(file, BytesIO):
        img = []
        buf = BufferedReader(file).read()
        img = cv.imdecode(np.frombuffer(buf, np.uint8), cv.IMREAD_COLOR)
        # img = cv.cvtColor(img, cv.COLOR_BGR2RGB) 不知这里为何不需要转换可能跟cv.imdecode有关

        size = img.shape # height: size[0], width: size[1], channel: size[2]
        img = cv.putText(img, label_name, (size[0]//8, size[1]//8), cv.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

        _, buffer = cv.imencode('.jpeg', img)
        img = base64.b64encode(buffer)

        return img
    else:
        return None

def stick_label_on_b64str(img_b64, label_name):
    img = str(img_b64).split(';base64,')[1]
    img = base64.b64decode(img)
    img = np.fromstring(img, np.uint8)
    img = cv.imdecode(img, cv.IMREAD_COLOR)

    size = img.shape # height: size[0], width: size[1], channel: size[2]
    img = cv.putText(img, label_name, (size[0]//8, size[1]//8), cv.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    _, buffer = cv.imencode('.jpeg', img)
    img = base64.b64encode(buffer)
    
    return img
