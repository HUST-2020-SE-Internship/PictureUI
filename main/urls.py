from django.urls import path, re_path

from main import views

app_name = 'main'

urlpatterns = [
    re_path(r'^homePage/$', views.homePage, name='homePage'),
    re_path(r'^account/(?P<pk>\d+)/explore/$', views.explore, name='Explore'),
    re_path(r'^account/(?P<pk>\d+)/classified/$', views.classified, name='Classified'),
    path('account/<int:pk>/classified/<str:typeName>/', views.classifiedSpecific, name='classifiedSpecific'),
    path('account/<int:pk>/classified/<str:typeName>/<str:subType>', views.subClassified, name="subClassified"),

    re_path(r'^account/(?P<pk>\d+)/personInfo/$', views.personInfo, name='PersonInfo'),
    re_path(r'^classify_test/$', views.classify_test, name='classify_test'),
    path('classify_img/', views.classify_img, name='classify_img'),
    
    re_path(r'^classify/$', views.classifyImage, name="classify"),
    re_path(r'^saveImage/$', views.saveImage, name='saveImage'),

    path('account/createSubFolder', views.createSubFolder, name='createSubFolder'),
    path('account/changeSubFolder', views.changeSubFolder, name='changeSubFolder'),
    path('account/removeImage', views.removeImage, name='removeImage'),
    path('account/moveImage', views.moveImage, name='moveImage'),
    path('account/updateIntroduction', views.updateIntroduction, name='updateIntroduction'),
    path('account/getTypeDict', views.getTypeDict, name="getTypeDict")
]
