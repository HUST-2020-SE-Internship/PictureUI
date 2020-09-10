from django.urls import path, re_path

from main import views

app_name = 'main'

urlpatterns = [
    re_path(r'^main/$', views.main,name='main'),
    re_path(r'^account/(?P<pk>\d+)/profile/$', views.profile, name='mainProfile'),
    re_path(r'^account/(?P<pk>\d+)/classifile/$', views.classify, name='mainClassifile'),
    re_path(r'^account/(?P<pk>\d+)/personInfo/$', views.personInfo, name='mainPersonInfo'),
    re_path(r'^classify/$', views.classify,name='classify'),

]