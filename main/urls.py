from django.urls import path, re_path

from main import views

app_name = 'main'

urlpatterns = [
    re_path(r'^main/$', views.main, name='main'),
    re_path(r'^account/(?P<pk>\d+)/profile/$', views.profile, name='mainProfile'),
    re_path(r'^account/(?P<pk>\d+)/classifile/$', views.classify, name='mainClassifile'),
    re_path(r'^account/(?P<pk>\d+)/classifile/person/$', views.classifilePerson, name='classifilePerson'),
    re_path(r'^account/(?P<pk>\d+)/classifile/point/$', views.classifilePoint, name='classifilePoint'),
    re_path(r'^account/(?P<pk>\d+)/classifile/video/$', views.classifileVideo, name='classifileVideo'),
    re_path(r'^account/(?P<pk>\d+)/classifile/scenery/$', views.classifileScenery, name='classifileScenery'),
    re_path(r'^account/(?P<pk>\d+)/classifile/cutScreen/$', views.classifileCutScreen, name='classifileCutScreen'),
    re_path(r'^account/(?P<pk>\d+)/personInfo/$', views.personInfo, name='mainPersonInfo'),
    re_path(r'^classify/$', views.classify, name='classify'),

]
