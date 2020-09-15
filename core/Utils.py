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