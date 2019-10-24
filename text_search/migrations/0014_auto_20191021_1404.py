# Generated by Django 2.2.4 on 2019-10-21 13:04

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('text_search', '0013_auto_20191020_2224'),
    ]

    operations = [
        migrations.CreateModel(
            name='AutocompleteForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('form', models.CharField(blank=True, default='', max_length=30)),
                ('lemma', models.CharField(default='', max_length=30)),
            ],
            managers=[
                ('from_kwic', django.db.models.manager.Manager()),
            ],
        ),
        migrations.DeleteModel(
            name='AutocompleteToken',
        ),
    ]
