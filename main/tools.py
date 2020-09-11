import os


# 读取函数，用来读取文件夹中的所有函数，输入参数是文件名
def read_directory(directory_name):

    listPicname = []
    for filename in os.listdir(directory_name):
        # 仅仅是为了测试
        picname = "/"+ directory_name + "/" + filename
        listPicname.append(picname)
    return listPicname
        ##img = cv2.imread(directory_name + "/" + filename)
        #####显示图片#######
        ##cv2.imshow(filename, img)
        ##cv2.waitKey(0)

