import base64
import json
import os

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404

from django.urls import reverse
from django.core.files.uploadedfile import InMemoryUploadedFile

from AutoAlbum.settings import MEDIA_URL
from main.tools import read_directory
from users.MyForms import ProfileForm
from users.models import UserProfile

from core import Classifier, AutoLabel, VGGLib

import copy

def main(request):
    if request.method == "POST":
        picStreamList = request.POST.get("picStreamList")
        picStreamList = json.loads(picStreamList)
        len = request.POST.get("len")
        i = 0
        picStreamList_data = []
        while i < int(len):
            picStream_data = str(picStreamList["pic" + str(i)]).split(';base64,')[1]
            data = base64.b64decode(picStream_data)
            picStreamList_data.append(data)
            i += 1
        ret = {"status": 0, 'url': ''}
        ret['status'] = 1
        ret['url'] = '/index/'
        return HttpResponse(json.dumps(ret))
    return render(request, 'main/main.html')

# 测试成功(该测试在后台调用classify_factory进行预测)
def classify_test(request):
    if request.method == "GET":
        # 处理访问该页面的普通GET请求
        return render(request, 'main/classify_test.html')
    elif request.method == "POST":
        # 处理ajax的POST请求 base64 strings
        img = request.POST.get("image")
        img_b64 = json.loads(img)
        result = Classifier.classify_factory.predict_by_b64str(img_b64)
        
        # 将预测后得到的标签贴在原图左上角
        labeled_img = AutoLabel.stick_label_on_b64str(img_b64, result)
        return HttpResponse(labeled_img, content_type="image/jpeg")

# for tensorflow source file:  io.BytesIO Object
def classify_img(request):
    if request.method == "POST":
        # print(type(img))
        # 这里的img为InMemoryUploadedFile对象，它的一个属性file为io.BytesIO Object
        # 使用cv.imdecode将其转换为ndaraay
        # InMemoryUploadedFile还有其他属性 DEBUG模式断点到此查看
        img = request.FILES['img']
        result = Classifier.classify_factory.predict_by_bytes(img.file)
        # labeled_img = AutoLabel.stick_label(file_copy, result)
        return JsonResponse({"status":"1","label": result})
    else:
        return JsonResponse({"status":"0"})

# for torch
def classifyImage(request):
    if request.method == "POST":
        image = request.POST.get("image")
        image = json.loads(image)
        result = VGGLib.classifyImage(image)
    return HttpResponse(json.dumps(result))

def saveImage(request):
    typeName = request.POST.get("typeName")
    image = request.POST.get("image")
    fileName = hash(image)
    image = json.loads(image)
    image = str(image).split(';base64,')[1]
    image = base64.b64decode(image)

    path = "media/" + request.user.username + "/" + typeName
    print(path, os.path.exists(path))
    if not os.path.exists(path):
        os.makedirs(path)

    filePath = os.path.join(path, str(fileName) + ".jpg")
    file = open(filePath, "wb")
    file.write(image)
    file.close()

    print("save => ", filePath)
    return HttpResponse("success")

def profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    url = MEDIA_URL + user.profile.portrait.name
    return render(request, 'main/main.html', {'user': user, 'url': url})

# 获取用户自己分类的图片信息,返回前端
def classified(request, pk):
    user = get_object_or_404(User, pk=pk)
    username = user.username
    # TODO:从数据库拿路径
    # 直接返回存储在云端media文件夹中的各文件路径
    urls = {}
    for root, dirs, files in os.walk("./media/"+username):
        for dir in dirs:
            urls[dir] = []
        for filename in files:
            img_name, img_ext = filename.split(".")
            if img_ext not in ['jpg','jpeg','png','bmp']:
                continue
            class_name = root.split("/media/" + username + '\\')[1] # 拿到图片的分类名与urls里的dir名对应
            urls[class_name].append(root[1:] + "/" + filename)

    return render(request, 'main/classified.html', {'user': user, 'urls': urls})

def classifiedPerson(request, pk):
    user = get_object_or_404(User, pk=pk)
    listPicname = read_directory("media/"+user.username+"/photo/person")
    url = MEDIA_URL + user.profile.portrait.name
    return render(request, 'main/classes/person.html', {'user': user, 'url': url, 'listPicname': listPicname})


def classifiedLocation(request, pk):
    user = get_object_or_404(User, pk=pk)
    listPicname = read_directory("media/" + user.username + "/photo/location")
    url = MEDIA_URL + user.profile.portrait.name
    return render(request, 'main/classes/location.html', {'user': user, 'url': url, 'listPicname': listPicname})


def classifiedVideo(request, pk):
    user = get_object_or_404(User, pk=pk)
    listPicname = read_directory("media/" + user.username + "/photo/video")
    url = MEDIA_URL + user.profile.portrait.name
    return render(request, 'main/classes/video.html', {'user': user, 'url': url, 'listPicname': listPicname})


def classifiedScenery(request, pk):
    user = get_object_or_404(User, pk=pk)
    listPicname = read_directory("media/" + user.username + "/photo/scenery")
    url = MEDIA_URL + user.profile.portrait.name
    return render(request, 'main/classes/scenery.html', {'user': user, 'url': url, 'listPicname': listPicname})


def classifiedScreenShot(request, pk):
    user = get_object_or_404(User, pk=pk)
    listPicname = read_directory("media/" + user.username + "/photo/screenshot")
    url = MEDIA_URL + user.profile.portrait.name
    return render(request, 'main/classes/screenshot.html', {'user': user, 'url': url, 'listPicname': listPicname})

def personInfo(request, pk):
    user = get_object_or_404(User, pk=pk)
    user_profile = get_object_or_404(UserProfile, user=user)
    url = MEDIA_URL + user.profile.portrait.name
    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILES)

        if form.is_valid():
            user_profile.org = form.cleaned_data['org']
            user_profile.telephone = form.cleaned_data['telephone']
            img = request.FILES.get("filepic")
            user_profile.portrait = img
            user_profile.save()

            return HttpResponseRedirect(reverse('main:profile', args=[user.id]))
    else:
        default_data = {'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email,
                        'org': user_profile.org, 'telephone': user_profile.telephone, 'username': user.username}
        form = ProfileForm(default_data)
    return render(request, 'main/personInfo.html', {'form': form, 'user': user, 'url': url})
