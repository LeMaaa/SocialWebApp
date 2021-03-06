# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-17 00:36
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('posts_title', models.CharField(max_length=100)),
                ('posts_content', models.TextField(max_length=160)),
                ('post_time', models.DateTimeField(auto_now_add=True)),
                ('last_modified_time', models.DateTimeField(auto_now=True, verbose_name='ModifiedTime')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.FileField(blank=True, upload_to='images')),
                ('file_type', models.CharField(max_length=50)),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('userage', models.IntegerField()),
                ('ip_addr', models.GenericIPAddressField()),
                ('friends', models.ManyToManyField(related_name='friends', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
