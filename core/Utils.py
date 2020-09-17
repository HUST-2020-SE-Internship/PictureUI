import os
from django.utils import timezone

initial_classes = ['person','location', 'scenery', 'video', 'screenshot',
                   'fruits', 'cat', 'dog', 'memory', 'spectacle', 'unknown']

classes_dict = {'person': ['person'],
                'location': ['house', 'railway', 'market', 'arch bridge', 'arch door'],
                'scenery': ['beach', 'mountain', 'landscape'],
                'fruits': ['banana', 'lemon', 'orange'],
                'cat': ['cat'],
                'dog': ['dog'],
                'memory': ['bottle', 'chair', 'volleyball', 'water pot', 'clothes'],
                'car':['car'],
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
        picname = "/"+ directory_name + "/" + filename
        listPicname.append(picname)
    return listPicname

# 获取某用户所有分类过的图片,带有子分类的图片无视子分类,归于其大类之下
def get_total_img_urls(username):
    urls = {}
    for root, dirs, files in os.walk("./media/"+username):
        for dir in dirs:
            urls[dir] = []
        for filename in files:
            _, img_ext = filename.split(".")
            if img_ext not in ['jpg','jpeg','png','bmp']:
                continue
            class_name = root.split("/media/" + username + '\\')[1] # 拿到图片的分类名与urls里的dir名对应
            if '\\' in class_name: # 若其含有子分类的目录,忽略子分类,采用根目录名称
                class_name = class_name.split('\\')[0]

            urls[class_name].append(root[1:] + "/" + filename)
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