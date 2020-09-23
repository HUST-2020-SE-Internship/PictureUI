from django.contrib import admin

# Register your models here.
from main.models import LabeledImage, ClassifiedType
from users.models import UserProfile

admin.site.register(LabeledImage)
admin.site.register(ClassifiedType)
admin.site.register(UserProfile)