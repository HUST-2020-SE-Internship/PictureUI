# Generated by Django 3.1.1 on 2020-09-10 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_userprofile_portrait'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='portrait',
            field=models.ImageField(blank=True, default='media/default.png', null=True, upload_to='photo'),
        ),
    ]