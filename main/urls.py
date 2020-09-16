from django.urls import path, re_path

from main import views

app_name = 'main'

urlpatterns = [
    re_path(r'^main/$', views.main, name='main'),
    re_path(r'^account/(?P<pk>\d+)/profile/$', views.profile, name='Profile'),
    re_path(r'^account/(?P<pk>\d+)/classified/$', views.classified, name='Classified'),
    re_path(r'^account/(?P<pk>\d+)/classified/person/$', views.classifiedPerson, name='classifiedPerson'),
    re_path(r'^account/(?P<pk>\d+)/classified/location/$', views.classifiedLocation, name='classifiedLocation'),
    re_path(r'^account/(?P<pk>\d+)/classified/video/$', views.classifiedVideo, name='classifiedVideo'),
    re_path(r'^account/(?P<pk>\d+)/classified/scenery/$', views.classifiedScenery, name='classifiedScenery'),
    re_path(r'^account/(?P<pk>\d+)/classified/screenshot/$', views.classifiedScreenShot, name='classifiedScreenShot'),
    re_path(r'^account/(?P<pk>\d+)/personInfo/$', views.personInfo, name='PersonInfo'),
    re_path(r'^account/(?P<pk>\d+)/classified/{typeName}$', views.personInfo, name='PersonInfo'),
    re_path(r'^classify_test/$', views.classify_test, name='classify_test'),
    path('classify_img/', views.classify_img, name='classify_img'),
    
    re_path(r'^classify/$', views.classifyImage, name="classify"),
    re_path(r'^saveImage/$', views.saveImage, name='saveImage'),
]
