from django.db import models

from django.contrib.auth.models import User

'''
'''

class LabeledImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="图片拥有者")
    root_type = models.CharField(max_length=50, verbose_name="根分类")
    sub_type = models.CharField(default='', max_length=50, verbose_name="子分类")
    img_name = models.CharField(max_length=255, verbose_name="图片名")

    class Meta:
        verbose_name = "Labeled Image Profile"

    def __str__(self):
        return self.user.username + "/" + self.root_type + "/" + self.sub_type + "/" + self.img_name

class ClassifiedType(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="分类拥有者")
    root_type = models.CharField(max_length=50, verbose_name="根分类")
    sub_type = models.CharField(default='', max_length=50, verbose_name="子分类")
    introduction = models.TextField(default='这个人很懒, 竟然不写简介', verbose_name="分类简介")

    class Meta:
        verbose_name = "Classified root_type and sub_type"