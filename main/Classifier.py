import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model_path = BASE_DIR+"NetModel/"

class Classifier:
    def __init__(self, model_name, img_size=(64,64)):
        self.model_name = model_name
        self.model = keras.models.load_model(model_path + model_name)

if __name__ == "__main__":
    pass