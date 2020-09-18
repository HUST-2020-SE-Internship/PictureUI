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
                if not os.path.isdir(subPath):
                    continue
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

# 获取某用户所有分类过的图片,带有子分类的图片无视子分类,归于其大类之下
def get_total_img_urls(username):
    urls = {}
    random.shuffle(initial_classes) # 打乱列表,使其被读入字典时顺序随机,以达成前端随机九个种类的显示
    for typename in initial_classes:
        urls[typename] = []
    for root, dirs, files in os.walk("./media/"+username):
        for filename in files:
            _, img_ext = filename.split(".")
            if img_ext not in ['jpg','jpeg','png','bmp']:
                continue
            class_name = root.split("/media/" + username + '\\')[1] # 拿到图片的分类名与urls里的dir名对应
            if '\\' in class_name: # 若其含有子分类的目录,忽略子分类,采用根目录名称
                class_name = class_name.split('\\')[0]
            img_url = root[1:] + "/" + filename
            img_url = img_url.replace('\\', '/')
            urls[class_name].append(img_url)
    return urls

# 获取某分类文件下的所有图片,包括根目录下与子分类文件夹下的图片
def get_specific_urls(userName, typeName):
    urls = {}
    urls[typeName] = [] # 用户某分类存储根路径下的img的list
    is_in_root = True
    root_path = None
    for root, dirs, files in os.walk("./media/" + userName + "/" + typeName):
        # 读取子分类subTypeName 文件夹结构 /media/{username}/{typeName}/{subtypeName} or {img}
        for dir in dirs:
            urls[dir] = []
        if is_in_root: # 第一次读取到得的是没有不在子分类文件夹下的img，若其不为空也需要返回
            for filename in files:
                _, img_ext = filename.split(".")
                if img_ext not in ['jpg','jpeg','png','bmp']:
                    continue
                urls[typeName].append(root[1:] + "/" + filename)
            is_in_root = False
            root_path = root
        else:
            subTypeName = root[len(root_path) + 1:] # 拿到图片的分类名与urls里的dir名对应
            for filename in files:
                _, img_ext = filename.split(".")
                if img_ext not in ['jpg','jpeg','png','bmp']:
                    continue
                urls[subTypeName].append(root[1:] + "/" + filename)

    return urls
