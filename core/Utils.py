import os
from django.utils import timezone
import base64
import random

from aip import AipFace

""" 你的 APPID AK SK """
APP_ID = '22675551'
API_KEY = 'fWRFhcsvO3VqaO9LHqur5HGG'
SECRET_KEY = 'nCfkdwd5ZGjBEZCnsUN8kqZFCQMXEYqA'

client = AipFace(APP_ID, API_KEY, SECRET_KEY)

initial_classes = ['person', 'location', 'scenery', 'video', 'screenshot',
                   'fruits', 'cat', 'dog', 'memory', 'spectacle', 'unknown']

classes_dict = {'person': ['person'],
                'location': ['house', 'railway', 'market', 'arch bridge', 'arch door'],
                'scenery': ['beach', 'mountain', 'landscape'],
                'fruits': ['banana', 'lemon', 'orange'],
                'cat': ['cat'],
                'dog': ['dog'],
                'memory': ['bottle', 'chair', 'volleyball', 'water pot', 'clothes'],
                'car': ['car'],
                'spectacle': ['rocket']}


# 为新用户创建基础分类文件夹
def create_user_media(username):
    for typeName in initial_classes:
        path = "media/" + username + "/" + typeName
        print(path, os.path.exists(path))
        if not os.path.exists(path):
            os.makedirs(path)


# 对上传的图片分类后进行保存
def auto_classified_storage(userName, typeName, image):
    modified_type = 'unknown'
    # 整合进预留标签对应的分类文件夹
    for (true_type, typeList) in classes_dict.items():
        if typeName in typeList:
            modified_type = true_type
            break

    path = "media/" + userName + "/" + modified_type
    print(path, os.path.exists(path))
    if not os.path.exists(path):
        os.makedirs(path)

    # 人脸分类调用百度api
    if modified_type == "person":
        dirs = os.listdir(path)
        if len(dirs) == 0:
            path = path + "/person_" + str(timezone.now().strftime("%Y-%m-%d_%H%M%S") + "_" + str(random.randint(0, 100)))
            os.makedirs(path)
            print("=== create new person dir: " + path)
        else:
            isClassify = False
            for subDir in dirs:
                subPath = os.path.join(path, subDir)
                imgs = os.listdir(subPath)
                for img in imgs:
                    imgPath = os.path.join(subPath, img)
                    result = client.match([
                        {
                            'image': str(base64.b64encode(image), 'utf-8'),
                            'image_type': 'BASE64',
                        },
                        {
                            'image': str(base64.b64encode(open(imgPath, 'rb').read()), 'utf-8'),
                            'image_type': 'BASE64',
                        }
                    ])
                    if result['error_msg'] == "SUCCESS" and result['result']['score'] > 70:
                        isClassify = True
                        path = subPath
                        print("=== match person dir: " + path)
                        break
                if isClassify:
                    break
            if not isClassify:
                path = path + "/person_" + str(timezone.now().strftime("%Y-%m-%d_%H%M%S") + "_" + str(random.randint(0, 100)))
                os.makedirs(path)
                print("=== [Not Match] create new person dir: " + path)

    # hash编码其图片名
    fileName = hash(image)
    filePath = os.path.join(path, str(fileName) + ".jpg")
    file = open(filePath, "wb")
    file.write(image)
    file.close()

    print("%s [USER]%s uploaded image saved! => %s" % (timezone.now().strftime("[%d/%b/%Y %H:%M:%S]"),
                                                       userName,
                                                       filePath))


# 读取函数，用来读取文件夹中的所有函数，输入参数是文件名
def read_directory(directory_name):
    listPicname = []
    for filename in os.listdir(directory_name):
        # 仅仅是为了测试
        picname = "/" + directory_name + "/" + filename
        listPicname.append(picname)
    return listPicname
