import os
from os import mkdir

from django.shortcuts import render, HttpResponse, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse
from django.utils import timezone

from .MyForms import RegistrationForm, LoginForm, ProfileForm, PwdChangeForm
from .models import UserProfile
from core import Utils

# Create your views here.

def index(request):
    print("index  doing")
    return HttpResponse("index  OK")

def profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'users/profile.html', {'user': user})

def profile_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    user_profile = get_object_or_404(UserProfile, user=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST)

        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()

            user_profile.org = form.cleaned_data['org']
            user_profile.telephone = form.cleaned_data['telephone']
            user_profile.save()

            return HttpResponseRedirect(reverse('users:profile', args=[user.id]))
    else:
        default_data = {'first_name': user.first_name, 'last_name': user.last_name,
                        'org': user_profile.org, 'telephone': user_profile.telephone, }
        form = ProfileForm(default_data)

    return render(request, 'users/profile_update.html', {'form': form, 'user': user})

'''
    标识符: is_in_register控制前端login或register容器的活跃状态
    缺省为False 即默认处于登录子页面下
'''
def register(request): 
    login_form = LoginForm()
    if request.method == 'GET': # GET方式访问gate/register模块
        register_form = RegistrationForm()
        return render(request, 'users/gate.html', {'login_form': login_form, 'register_form': register_form, 'is_in_register': True})
    elif request.method == 'POST': # 处理register功能的POST请求
        register_form = RegistrationForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password2']

            # 使用内置User自带create_user方法创建用户，不需要使用save()
            user = User.objects.create_user(username=username, password=password, email=email)
            Utils.create_user_media(username)

            # 如果直接使用objects.create()方法后不需要使用save()
            user_profile = UserProfile(user=user)
            user_profile.save()

            return render(request, 'users/gate.html', {'login_form': login_form, 'register_form': register_form, 'register_success': True})
        else:
            return render(request, 'users/gate.html', {'login_form': login_form, 'register_form': register_form, 'is_in_register': True})

def login(request):
    if request.method == 'GET': # GET方式访问gate/login模块
        login_form = LoginForm()
        register_form = RegistrationForm()

        redirect_from_auth = False
        if request.session.get('redirect_from_auth'): # 控制显示"请登录"
            redirect_from_auth = True
            request.session['redirect_from_auth'] = False

        return render(request, 'users/gate.html', {'login_form': login_form, 
                                                    'register_form': register_form, 
                                                    'redirect_from_auth':redirect_from_auth})
    elif request.method == 'POST':
        login_form = LoginForm(request.POST)
        register_form = RegistrationForm()
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            user = auth.authenticate(username=username, password=password)

            if user is not None and user.is_active:  # 登录成功,跳转
                auth.login(request, user)
                # 输出登录日志
                print("%s [USER]%s logged in @ %s" % (timezone.localtime(user.last_login).strftime("[%d/%b/%Y %H:%M:%S]"), 
                                                        user.username, 
                                                        get_IP(request)))

                return HttpResponseRedirect(reverse('main:homePage'))
            else:
                # 用户名/邮箱存在于数据库,但是密码错误
                login_form.add_error("password", "密码错误")
                return render(request, 'users/gate.html',{'login_form': login_form, 'register_form': register_form})
        else:
            # 登录失败，用户名/邮箱不存在
            return render(request, 'users/gate.html', {'login_form': login_form, 'register_form': register_form})

# 获取用户的IP地址
def get_IP(request):
    # 获取HTTP请求端的XFF头，在META信息中只有通过了HTTP代理或者负载均衡服务器后才会出现该项
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    if xff:
        ip = xff.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def logout(request): # 若用户未登录,auth.logout(request)也不会报错
    auth.logout(request)
    return HttpResponseRedirect("/users/login/")

def pwd_change(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.method == "POST":
        form = PwdChangeForm(request.POST)

        if form.is_valid():
            password = form.cleaned_data['old_password']
            username = user.username

            user = auth.authenticate(username=username, password=password)

            if user is not None and user.is_active:
                new_password = form.cleaned_data['password2']
                user.set_password(new_password)
                user.save()
                return HttpResponseRedirect('/users/login/')

            else:
                return render(request, 'users/pwd_change.html', {'form': form,
                                                                 'user': user,
                                                                 'message': 'Old password is wrong Try again'})
    else:
        form = PwdChangeForm()

    return render(request, 'users/pwd_change.html', {'form': form, 'user': user})
