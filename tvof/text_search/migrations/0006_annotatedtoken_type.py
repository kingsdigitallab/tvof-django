# Generated by Django 2.2.4 on 2019-09-17 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('text_search', '0005_auto_20190917_1931'),
    ]

    operations = [
        migrations.AddField(
            model_name='annotatedtoken',
            name='type',
            field=models.CharField(default='', max_length=30),
        ),
    ]
