# Generated by Django 2.1.7 on 2019-02-18 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('text_search', '0002_auto_20181118_2039'),
    ]

    operations = [
        migrations.AddField(
            model_name='annotatedtoken',
            name='lemmapos',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
    ]
