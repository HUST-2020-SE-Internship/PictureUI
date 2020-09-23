import os
from django.utils import timezone
import base64
import random
import cv2
import numpy as np

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from main.models import ClassifiedType, LabeledImage

from aip import AipFace

""" 你的 APPID AK SK """
APP_ID = '22675551'
API_KEY = 'fWRFhcsvO3VqaO9LHqur5HGG'
SECRET_KEY = 'nCfkdwd5ZGjBEZCnsUN8kqZFCQMXEYqA'

client = AipFace(APP_ID, API_KEY, SECRET_KEY)

options = {"max_face_num": 10,
           "face_type": "LIVE",
           "liveness_control": "LOW"}
imageType = "BASE64"

initial_classes = ['person', 'location', 'scenery', 'car', 'screenshot',
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

def create_user_classifiedtype(user):
    for typeName in initial_classes:
        user_classifiedtype = ClassifiedType(user=user)
        user_classifiedtype.root_type = typeName
        user_classifiedtype.save()

# 为新用户创建基础分类文件夹
def create_user_media(username):
    for typeName in initial_classes:
        path = "media/" + username + "/" + typeName
        print(path, os.path.exists(path))
        if not os.path.exists(path):
            os.makedirs(path)


# 对上传的图片分类后进行保存
def auto_classified_storage(userName, typeName, image):
    user = get_object_or_404(User, username=userName)
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

    fileName = str(hash(image)) + ".jpg"
    sub_type=''

    # 人脸分类调用百度api
    if modified_type == "person":
        dirs = os.listdir(path)
        # 获取人脸位置信息
        imageBase64 = str(base64.b64encode(image), 'utf-8')
        result = client.detect(imageBase64, imageType, options)
        # image转换为cv2格式
        img_array = np.fromstring(image, np.uint8)  # 转换np序列
        image = cv2.imdecode(img_array, cv2.COLOR_BGR2RGB)
        # 获取所有标准人脸截图
        faceImages = []
        if result.get("result") is not None:
            result = result["result"]
            face_list = result["face_list"]
            rows, cols = image.shape[:2]
            for face in face_list:
                location = face["location"]
                left = (int(location["left"]), int(location["top"]))
                right = (int(location["left"] + location["width"]), int(location["top"] + location["height"]))
                M = cv2.getRotationMatrix2D(left, location["rotation"], 1)
                imgTmp = cv2.warpAffine(image, M, (cols, rows))
                res = imgTmp[left[1]:right[1], left[0]:right[0]]
                faceImages.append(res)
        for faceImage in faceImages:
            isClassify = False
            # 获取人脸分类子文件夹
            for subDir in dirs:
                subPath = os.path.join(path, subDir)
                if not os.path.isdir(subPath):
                    continue
                standardImage = os.path.join(subPath, "standard.jpg")
                if not os.path.exists(standardImage):
                    print("[NULL] standard not found: ", standardImage)
                    continue
                res = client.match([
                    {
                        'image': str(cv2_base64(faceImage), 'utf-8'),
                        'image_type': 'BASE64',
                    },
                    {
                        'image': str(base64.b64encode(open(standardImage, 'rb').read()), 'utf-8'),
                        'image_type': 'BASE64',
                    }
                ])
                if res['error_msg'] == "SUCCESS" and res['result']['score'] > 70:
                    isClassify = True
                    filePath = os.path.join(subPath, fileName)
                    cv2.imwrite(filePath, image)
                    print("[PERSON ADD] save %s" % filePath)
                    
                    # 表中插入记录
                    sub_type = subDir
                    ClassifiedType.objects.get_or_create(user=user, root_type=modified_type, sub_type=sub_type)
                    LabeledImage.objects.create(user=user, root_type=modified_type, sub_type=sub_type, img_name=fileName)
                    break
                elif res['error_msg'] == "SUCCESS":
                    print("dir: %s => %s" % (str(subDir), str(res['result']['score'])))
                else:
                    print("%s pass %s" % (str(subDir), res))
            if not isClassify:
                sub_type = "person_" + str(
                    timezone.now().strftime("%Y-%m-%d_%H%M%S") + "_" + str(random.randint(0, 100)))
                newDirpath = os.path.join(path, sub_type)
                os.makedirs(newDirpath)
                cv2.imwrite(os.path.join(newDirpath, "standard.jpg"), faceImage)
                filePath = os.path.join(newDirpath, fileName)
                cv2.imwrite(filePath, image)
                print("[PERSON NEW] save %s" % filePath)

                # 插入记录
                ClassifiedType.objects.get_or_create(user=user, root_type=modified_type, sub_type=sub_type)
                LabeledImage.objects.create(user=user, root_type=modified_type, sub_type=sub_type, img_name=fileName)
    else:
        filePath = os.path.join(path, fileName)
        file = open(filePath, "wb")
        file.write(image)
        file.close()
        print("[NORMAL] save %s" % filePath)

        ClassifiedType.objects.get_or_create(user=user, root_type=modified_type, sub_type=sub_type)
        LabeledImage.objects.create(user=user, root_type=modified_type, sub_type=sub_type, img_name=fileName)

        # if len(dirs) == 0:
        #     path = path + "/person_" + str(timezone.now().strftime("%Y-%m-%d_%H%M%S") + "_" + str(random.randint(0, 100)))
        #     os.makedirs(path)
        #     print("=== create new person dir: " + path)
        #     # 添加标准图片
        # else:
        #     isClassify = False
        #     for subDir in dirs:
        #         subPath = os.path.join(path, subDir)
        #         if not os.path.isdir(subPath):
        #             continue
        #         imgs = os.listdir(subPath)
        #         for img in imgs:
        #             imgPath = os.path.join(subPath, img)
        #             result = client.match([
        #                 {
        #                     'image': str(base64.b64encode(image), 'utf-8'),
        #                     'image_type': 'BASE64',
        #                 },
        #                 {
        #                     'image': str(base64.b64encode(open(imgPath, 'rb').read()), 'utf-8'),
        #                     'image_type': 'BASE64',
        #                 }
        #             ])
        #             if result['error_msg'] == "SUCCESS" and result['result']['score'] > 70:
        #                 isClassify = True
        #                 path = subPath
        #                 print("=== match person dir: " + path)
        #                 break
        #         if isClassify:
        #             break
        #     if not isClassify:
        #         path = path + "/person_" + str(timezone.now().strftime("%Y-%m-%d_%H%M%S") + "_" + str(random.randint(0, 100)))
        #         os.makedirs(path)
        #         print("=== [Not Match] create new person dir: " + path)

    # hash编码其图片名
    # fileName = hash(image)
    # filePath = os.path.join(path, str(fileName) + ".jpg")
    # file = open(filePath, "wb")
    # file.write(image)
    # file.close()

    # print("%s [USER]%s uploaded image saved! => %s" % (timezone.now().strftime("[%d/%b/%Y %H:%M:%S]"),
    #                                                    userName,
    #                                                    filePath))


# 读取函数，用来读取文件夹中的所有函数，输入参数是文件名
def read_directory(directory_name):
    listPicname = []
    for filename in os.listdir(directory_name):
        # 仅仅是为了测试
        picname = "/" + directory_name + "/" + filename
        listPicname.append(picname)
    return listPicname


# 获取某用户所有分类过的图片,带有子分类的图片无视子分类,归于其大类之下
def get_total_img_urls(username):
    urls = {}
    random.shuffle(initial_classes)  # 打乱列表,使其被读入字典时顺序随机,以达成前端随机种类的显示
    for typename in initial_classes:
        urls[typename] = []
    for root, dirs, files in os.walk("./media/" + username):
        for filename in files:
            img_name, img_ext = filename.split(".")
            if img_ext not in ['jpg', 'jpeg', 'png', 'bmp'] or img_name == 'standard':
                continue
            class_name = root.split("/media/" + username + os.sep)[1]  # 拿到图片的分类名与urls里的dir名对应
            if os.sep in class_name:  # 若其含有子分类的目录,忽略子分类,采用根目录名称
                class_name = class_name.split(os.sep)[0]
            img_url = root[1:] + "/" + filename
            img_url = img_url.replace(os.sep, '/')
            urls[class_name].append(img_url)
    return urls


# 获取某分类文件下的所有图片,包括根目录下与子分类文件夹下的图片
def get_specific_urls(userName, typeName):
    urls = {}
    urls[typeName] = []  # 用户某分类存储根路径下的img的list
    is_in_root = True
    root_path = None
    for root, dirs, files in os.walk("./media/" + userName + "/" + typeName):
        # 读取子分类subTypeName 文件夹结构 /media/{username}/{typeName}/{subtypeName} or {img}
        for dir in dirs:
            urls[dir] = []
        if is_in_root:  # 第一次读取到得的是没有不在子分类文件夹下的img，若其不为空也需要返回
            for filename in files:
                _, img_ext = filename.split(".")
                if img_ext not in ['jpg', 'jpeg', 'png', 'bmp']:
                    continue
                urls[typeName].append(root[1:] + "/" + filename)
            is_in_root = False
            root_path = root
        else:
            subTypeName = root[len(root_path) + 1:]  # 拿到图片的分类名与urls里的dir名对应
            for filename in files:
                img_name, img_ext = filename.split(".")
                if img_ext not in ['jpg', 'jpeg', 'png', 'bmp'] or img_name == 'standard':
                    continue
                urls[subTypeName].append(root[1:] + "/" + filename)

    return urls

# 获取某分类文件夹下某子分类的所有图片
def get_subclassified_urls(userName, typeName, subType):
    urls = [] # 已经确定了分类及其子分类,直接使用list存储
    for root, dirs, files in os.walk("./media/" + userName + "/" + typeName + "/" + subType):
        # 读取子分类subTypeName 文件夹结构 /media/{username}/{typeName}/{subtypeName} or {img}
        for filename in files:
            img_name, img_ext = filename.split(".")
            if img_ext not in ['jpg', 'jpeg', 'png', 'bmp'] or img_name == 'standard':
                continue
            urls.append(root[1:] + "/" + filename)

    return urls

def cv2_base64(image):
    base64_str = cv2.imencode('.jpg', image)[1].tostring()
    base64_str = base64.b64encode(base64_str)
    return base64_str

def get_type_dict(user):
    # 这里的typedict不局限于当前typeName 是该用户所有的标签分类, 用于进行图片移动操作
    classified_type_infos = ClassifiedType.objects.filter(user=user)
    typedict = {}
    for info in classified_type_infos:
        if not typedict.get(info.root_type):
            typedict[info.root_type] = []
        if info.sub_type is not '':
            typedict[info.root_type].append(info.sub_type)

    return typedict

def get_random_photo(username):
    random.shuffle(initial_classes)
    photoDict = {}
    for typeName in initial_classes:
        for root, dirs, files in os.walk("./media/" + username + "/" + typeName):
            for filename in files:
                img_name, img_ext = filename.split(".")
                if img_ext not in ['jpg', 'jpeg', 'png', 'bmp'] or img_name == 'standard':
                    continue
                img_url = root[1:] + "/" + filename
                img_url = img_url.replace(os.sep, '/')
                photoDict[typeName] = img_url
                break
            if photoDict:
                break
        if photoDict:
            break

    return photoDict
            