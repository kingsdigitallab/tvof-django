# Generated by Django 2.2.4 on 2019-09-23 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('text_search', '0006_annotatedtoken_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='annotatedtoken',
            name='section_number',
            field=models.IntegerField(default=0),
        ),
    ]
