# Generated by Django 2.2.4 on 2019-09-17 18:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('text_search', '0004_auto_20190917_1908'),
    ]

    operations = [
        migrations.RenameField(
            model_name='annotatedtoken',
            old_name='token_number',
            new_name='n',
        ),
        migrations.RenameField(
            model_name='annotatedtoken',
            old_name='token',
            new_name='string',
        ),
    ]