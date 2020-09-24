from torch import nn
import torch
import cv2
import numpy as np
import base64
from aip import AipFace
from .Classifier import classify_factory

""" 你的 APPID AK SK """
APP_ID = '22675551'
API_KEY = 'fWRFhcsvO3VqaO9LHqur5HGG'
SECRET_KEY = 'nCfkdwd5ZGjBEZCnsUN8kqZFCQMXEYqA'

client = AipFace(APP_ID, API_KEY, SECRET_KEY)

""" 备选APP_ID """
APP_ID_2 = '22748271'
API_KEY_2 = 'gOvldKxiFLjXbbyc9bRcHyEb'
SECRET_KEY_2 = '4Qm7SFOUgZQqdHZ30iwu7wGt2TOR3nBe'

client_2 = AipFace(APP_ID_2, API_KEY_2, SECRET_KEY_2)

options = {"max_face_num": 1,
           "face_type": "LIVE",
           "liveness_control": "LOW"}
imageType = "BASE64"

USE_GPU = False
net = None
device = None
labelName = []


class VGGNet(nn.Module):
    def __init__(self, num_classes, init_weights=True):
        super(VGGNet, self).__init__()
        # 64
        self.conv1 = nn.Sequential(
            nn.Conv2d(in_channels=3, out_channels=64, kernel_size=3, stride=1, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(in_channels=64, out_channels=64, kernel_size=3, stride=1, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )
        # 32
        self.conv2 = nn.Sequential(
            nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, stride=1, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(in_channels=128, out_channels=128, kernel_size=3, stride=1, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )
        # 16
        self.conv3 = nn.Sequential(
            nn.Conv2d(in_channels=128, out_channels=256, kernel_size=3, stride=1, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(in_channels=256, out_channels=256, kernel_size=3, stride=1, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(in_channels=256, out_channels=256, kernel_size=3, stride=1, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )
        # 8
        self.conv4 = nn.Sequential(
            nn.Conv2d(in_channels=256, out_channels=512, kernel_size=3, stride=1, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(in_channels=512, out_channels=512, kernel_size=3, stride=1, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(in_channels=512, out_channels=512, kernel_size=3, stride=1, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )
        # 4
        self.conv5 = nn.Sequential(
            nn.Conv2d(in_channels=512, out_channels=512, kernel_size=3, stride=1, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(in_channels=512, out_channels=512, kernel_size=3, stride=1, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(in_channels=512, out_channels=512, kernel_size=3, stride=1, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )
        # 2
        self.avgpool = nn.AdaptiveAvgPool2d((2, 2))
        self.classifier = nn.Sequential(
            nn.Linear(512 * 2 * 2, 1000),
            nn.ReLU(inplace=True),
            nn.Dropout(),
            nn.Linear(1000, 1000),
            nn.ReLU(inplace=True),
            nn.Dropout(),
        )
        self.classifier2 = nn.Linear(1000, num_classes)
        if init_weights:
            self._initialize_weights()

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)
        x = self.conv4(x)
        x = self.conv5(x)
        x = self.avgpool(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        x = self.classifier2(x)
        return x

    def _initialize_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.Linear):
                nn.init.normal_(m.weight, 0, 0.01)
                nn.init.constant_(m.bias, 0)


def loadLabelName():
    global labelName
    with open("./core/NetModel/VGG/labelName.txt", encoding="utf-8") as file:
        for line in file:
            labelName.append(line.split("\t")[1].strip())
    return labelName


def classifyImage(img):
    if isPersonByBaidu(img):
        return "person"
    image = img
    img = preprocess(img)
    global net, device, labelName, USE_GPU
    if net is None:
        print("Loading Net...")
        if torch.cuda.is_available() and USE_GPU:
            USE_GPU = True
            device = torch.device("cuda:1")
            net = torch.load("./core/NetModel/VGG/net_tiny_final.pkl").to(device)
        else:
            net = torch.load("./core/NetModel/VGG/net_tiny_final.pkl", map_location=torch.device('cpu'))
        labelName = loadLabelName()
    img = cv2.resize(img, (64, 64), cv2.INTER_AREA)
    img = np.transpose(img, (2, 0, 1))
    img = torch.FloatTensor(img)
    img = img.unsqueeze(0)
    img = img / 255
    if USE_GPU:
        img = img.to(device)
    outputs = net(img)
    _, predicted = torch.max(outputs.data, 1)
    result = predicted[0].cpu().numpy()
    if labelName[result] == "cat" or labelName[result] == "dog":
        return str(classify_factory.predict_by_b64str(image)).lower()
    return labelName[result]


def preprocess(image):
    image = str(image).split(';base64,')[1]
    image = base64.b64decode(image)
    image = np.fromstring(image, np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image


def isPersonByBaidu(image):
    image = str(image).split(';base64,')[1]
    result = client.detect(image, imageType, options)
    print(result)
    if result.get("error_code") == 18: # 达到上限启用备选APP_ID
        result = client_2.detect(image, imageType, options)
    
    if result.get("result") is not None and result["result"] is not None:
        return True
    else:
        return False
