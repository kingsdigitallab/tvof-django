# Generated by Django 2.2.4 on 2019-10-02 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('text_search', '0008_auto_20191002_0033'),
    ]

    operations = [
        migrations.AddField(
            model_name='annotatedtoken',
            name='speech_cat',
            field=models.SmallIntegerField(default=0),
        ),
    ]
