# Generated by Django 3.1 on 2020-09-22 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20200921_1101'),
    ]

    operations = [
        migrations.AddField(
            model_name='classifiedtype',
            name='introduction',
            field=models.TextField(default='这个人很懒, 竟然不写简介', verbose_name='分类简介'),
        ),
    ]