# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-09 15:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AnnotatedToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=30)),
                ('preceding', models.CharField(max_length=200)),
                ('following', models.CharField(max_length=200)),
                ('lemma', models.CharField(max_length=30)),
                ('location', models.CharField(max_length=20)),
                ('token_number', models.IntegerField(help_text='The sequential index of the token relative to the seg')),
                ('pos', models.CharField(max_length=30)),
            ],
        ),
    ]
