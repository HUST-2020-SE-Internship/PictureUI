import base64
import json
import os, shutil

from django.contrib.auth.models import User
from django.conf import settings
from django.core.files.base import ContentFile

from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404

from django.urls import reverse
from django.core.files.uploadedfile import InMemoryUploadedFile

from AutoAlbum.settings import MEDIA_URL
from users.MyForms import ProfileForm
from users.models import UserProfile
from .models import LabeledImage, ClassifiedType

from core import Classifier, AutoLabel, VGGLib, Utils

import copy

def homePage(request):
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
    return render(request, 'main/homePage.html')

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
    image = json.loads(image)
    image = str(image).split(';base64,')[1]
    image = base64.b64decode(image)

    Utils.auto_classified_storage(request.user.username, typeName, image)

    return HttpResponse("success")

def explore(request, pk):
    user = get_object_or_404(User, pk=pk)

    return render(request, 'main/explore.html', {'user': user})

# 获取用户自己分类的图片信息,返回前端
def classified(request, pk):
    user = get_object_or_404(User, pk=pk)
    urls = Utils.get_total_img_urls(user.username)

    return render(request, 'main/classified_new.html', {'user': user, 'urls': urls})

def classifiedSpecific(request, pk, typeName):
    user = get_object_or_404(User, pk=pk)
    urls = Utils.get_specific_urls(user.username, typeName)
    typedict = Utils.get_type_dict(user)

    return render(request, 'main/classifiedSpecific.html', {'user': user, 'urls': urls, "typeName": typeName, "typeDict": typedict})

def subClassified(request, pk, typeName, subType):
    user = get_object_or_404(User, pk=pk)
    urls= Utils.get_subclassified_urls(user.username, typeName, subType)
    typedict = Utils.get_type_dict(user)
    introduction = get_object_or_404(ClassifiedType, user=user, root_type=typeName, sub_type=subType).introduction

    return render(request, 'main/subClassified.html', locals())

def createSubFolder(request):
    if request.method == 'POST':
        user = get_object_or_404(User, pk=request.session.get('_auth_user_id'))
        typeName = request.POST.get('typeName')
        subFolder = request.POST.get('subFolder')
        dst_path = settings.MEDIA_ROOT + user.username + "/" + typeName + "/" + subFolder
        if not os.path.exists(dst_path):
            os.mkdir(dst_path)
            # 表中新建记录
            classifiedtype = ClassifiedType.objects.create(user=user, root_type=typeName, sub_type=subFolder)

            return JsonResponse({"status":"1", "msg":"created new subfolder!"})
        else:
            return JsonResponse({"status":"0", "msg":"that folder already exists"})

def changeSubFolder(request):
    if request.method == "POST":
        user = get_object_or_404(User, pk=request.session.get('_auth_user_id'))
        typeName = request.POST.get('typeName')
        old_name = request.POST.get('old_name')
        new_name = request.POST.get('new_name')
        print("[USER]%s want to change [sub_typename]%s => %s in [type]%s" % (user.username, old_name, new_name, typeName))
        type_path = settings.MEDIA_ROOT + user.username + "/" + typeName + "/"
        if os.path.exists(type_path + old_name):
            os.rename(type_path + old_name, type_path + new_name)
            # 先在分类关系表中更改
            ClassifiedType.objects.filter(user=user, root_type=typeName, sub_type=old_name).update(sub_type=new_name)
            # 再到图片路径表中将所有原分类名全部改为新分类名
            LabeledImage.objects.filter(user=user, sub_type=old_name).update(sub_type=new_name)

            return JsonResponse({"status":"1", "msg":"更改成功"})
        else:
            return JsonResponse({"status":"0", "msg":"WTF?"})

def removeImage(request):
    if request.method == 'POST':
        user = get_object_or_404(User, pk=request.session.get('_auth_user_id'))
        typeName = request.POST.get('typeName')
        img_url = request.POST.get('img_url')
        # img_url likes Context_path + MEDIA_URL + ...
        # img_path likes MEDIA_ROOT + username + "/{typeName}/{subType}/img_name" or just "/{typeName}/img_name"
        img_path = os.path.join(settings.MEDIA_ROOT, img_url.split(settings.MEDIA_URL)[1])
        img_name = img_url.split("/"+typeName+"/")[1]
        if "/" in img_name: # 说明此时包含子分类名
            img_name = img_name.split("/")[1] # 切割子分类, 拿到第二个即图片的真实name

        if os.path.exists(img_path):
            os.remove(img_path)
            # 从表中删除
            LabeledImage.objects.filter(user=user, img_name=img_name).delete()

            return JsonResponse({"status":"1"})
        else:
            return JsonResponse({"status":"0", "msg":"That Image does not exist?"})

def moveImage(request):
    if request.method == "POST":
        user = get_object_or_404(User, pk=request.session.get('_auth_user_id'))
        root_type = request.POST.get('root_type')
        sub_type = request.POST.get('sub_type')
        old_root_type = request.POST.get('old_root_type')
        img_url = request.POST.get('img_url')
        # 组装为本地图片存储路径
        old_path = os.path.join(settings.MEDIA_ROOT, img_url.split(settings.MEDIA_URL)[1])
        img_name = img_url.split("/"+old_root_type+"/")[1]
        if "/" in img_name: # 说明此时包含子分类名
            img_name = img_name.split("/")[1] # 切割子分类, 拿到第二个即图片的真实name
        
        new_path = os.path.join(settings.MEDIA_ROOT, user.username, root_type)
        if sub_type == '':
            new_path = os.path.join(new_path, img_name)
        else:
            new_path = os.path.join(new_path, sub_type, img_name)
        if os.path.exists(old_path) and not os.path.exists(new_path):
            shutil.move(old_path, new_path)
            # 更新相关表
            LabeledImage.objects.filter(user=user, img_name=img_name).update(root_type=root_type, sub_type=sub_type)
            return JsonResponse({"status":"1", "msg":"success"})
        else:
            return JsonResponse({"status":"0", "msg":"There is sth. going wrong"})

def updateIntroduction(request):
    if request.method == 'POST':
        user = get_object_or_404(User, pk=request.session.get('_auth_user_id'))
        typeName = request.POST.get('typeName')
        subType = request.POST.get('subType')
        new_intro = request.POST.get('new_intro')
        
        # 更新表
        ClassifiedType.objects.filter(user=user, root_type=typeName, sub_type=subType).update(introduction=new_intro)

        return JsonResponse({"status":"1", "msg":"success"})
    else:
        return JsonResponse({"status":"0", "msg":"There is sth. going wrong"})

def personInfo(request, pk):
    user = get_object_or_404(User, pk=pk)
    user_profile = get_object_or_404(UserProfile, user=user)
    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILES)
        nickName = request.POST.get("nickName")
        telephone = request.POST.get("telephone")
        image = request.POST.get("image")
        if image is not None:
            image = json.loads(image)
            user_profile.portrait = image
            print(image)
        #imagene = ContentFile(image, 'imagen1.png')
        user_profile.org = nickName
        user_profile.telephone = telephone
        user_profile.save()
        # if form.is_valid():
        #     user_profile.org = form.cleaned_data['org']
        #     user_profile.telephone = form.cleaned_data['telephone']
        #     img = request.FILES.get("filepic")
        #     user_profile.portrait = img
        #     user_profile.save()

        return render(request, 'main/personInfo.html', { 'user': user})
    else:
        default_data = {'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email,
                        'org': user_profile.org, 'telephone': user_profile.telephone, 'username': user.username}
        form = ProfileForm(default_data)
    return render(request, 'main/personInfo.html', {'user': user})
