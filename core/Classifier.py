import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator

import os
import numpy as np 
import cv2 as cv

from io import BufferedReader, BytesIO
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 启动Django项目时,会初始化该类,加载模型耗时较长但是加载完毕后该实例一直留在资源池中等待调用
# 在此类中编写接口即可
# 包括 根据图片识别,根据numpy组成的数组识别等
class Classifier:
    def __init__(self, model_dir, model_name, img_size=(160,160)):
        self.img_size = img_size
        self.model_dir = model_dir
        self.model_name = model_name
        self.model = keras.models.load_model(BASE_DIR + model_dir + model_name)
        # 模型加载完毕后立即使用一次Model.predict初始化模型
        self.model.predict(np.zeros((1,160,160,3)))

        # 读取标签映射
        self.label_names = []
        with open(BASE_DIR + model_dir + "/label_mapping.txt", encoding="utf-8") as mappings:
            for mapping in mappings:
                mapping = mapping.strip("\n")
                print("读取到 %s " % mapping)
                self.label_names.append(mapping.split('\t')[1])

        '''TODO:Init ImageDataGenerator 
        self.dst_images_formatter = ImageDatagenerator()

        '''
    
    def predict_by_imgpath(self, path):
        test_images = []
        true_names = []
        for root, _, files in os.walk(path):
            for filename in files:
                img_name, img_ext = os.path.splitext(filename)
                if img_ext.lower() not in ['.jpg','.jpeg','.bmp','.png']:
                    break
                img = cv.imread(os.path.join(root, filename))
                img = cv.resize(img, self.img_size, cv.INTER_AREA)
                true_names.append(img_name)
                test_images.append(img)

        # 归一化 0~255 => -1~1
        test_images = np.array(test_images)
        test_images = test_images.astype("float32") / 127.5 - 1

        predictions = self.model.predict(test_images)

        for i, prediction in enumerate(predictions):
            predicted_label = 0 if prediction[0] < 0 else 1
            print("[True Class] %s <= => %s [Predict result: %0.6f] " % (true_names[i], self.label_names[predicted_label], prediction[0]))

    def predict_test(self):
        test_path = BASE_DIR + "/core/NetModel/test"
        self.predict_by_imgpath(test_path)

    def predict_by_bytes(self, file):
        img = self.temporary_img_format(file)

        predictions = self.model.predict(img)
        predicted_label = 0 if predictions[0] < 0 else 1
        return self.label_names[predicted_label]

    # TODO: 临时图片格式化函数, 不远的将来需使用ImageDataGenerator
    def temporary_img_format(self, file):
        img = []
        if isinstance(file, BytesIO):
            buf = BufferedReader(file).read()
            img = cv.imdecode(np.frombuffer(buf, np.uint8), cv.IMREAD_COLOR)
            img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
            img = cv.resize(img, self.img_size, cv.INTER_AREA)
        elif type(file) is np.ndarray:
            img = file

        # 处理为网络模型需求的输入
        img = np.array(img)
        img = img.astype("float32") / 127.5 - 1
        img = np.expand_dims(img, axis = 0)

        return img

classify_factory = Classifier("/core/NetModel/MobileNetV2/", "MobileNetV2_binary_fine.h5")

if __name__ == "__main__":
    
    test_path = BASE_DIR + "/core/NetModel/test"
    classify_factory.predict_by_imgpath(test_path)

    