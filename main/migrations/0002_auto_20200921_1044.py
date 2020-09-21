# Generated by Django 3.1 on 2020-09-21 02:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='labeledimage',
            options={'verbose_name': 'Labeled Image Profile'},
        ),
        migrations.CreateModel(
            name='ClassifiedType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('root_type', models.CharField(max_length=50, verbose_name='根分类')),
                ('sub_type', models.CharField(default='', max_length=50, verbose_name='子分类')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='分类拥有者')),
            ],
            options={
                'verbose_name': 'Classified root_type and sub_type',
            },
        ),
    ]