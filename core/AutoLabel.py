import numpy as np
import cv2 as cv
import base64

from io import BufferedReader, BytesIO

def stick_label(file, label_name):
    img = []
    if isinstance(file, BytesIO):
        buf = BufferedReader(file).read()
        img = cv.imdecode(np.frombuffer(buf, np.uint8), cv.IMREAD_COLOR)
        # img = cv.cvtColor(img, cv.COLOR_BGR2RGB) 不知这里为何不需要转换可能跟cv.imencode有关
    elif type(file) is np.ndarray:
        img = file

    size = img.shape # height: size[0], width: size[1], channel: size[2]
    img = cv.putText(img, label_name, (50,50), cv.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)


    retval, buffer = cv.imencode('.jpeg', img)
    img = base64.b64encode(buffer)

    return img
