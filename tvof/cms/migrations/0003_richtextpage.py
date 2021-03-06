# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-11 13:09


from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0028_merge'),
        ('cms', '0002_create_homepage'),
    ]

    operations = [
        migrations.CreateModel(
            name='RichTextPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('content', wagtail.core.fields.StreamField([(b'heading', wagtail.core.blocks.CharBlock(classname=b'')), (b'paragraph', wagtail.core.blocks.RichTextBlock()), (b'image', wagtail.images.blocks.ImageChooserBlock())])),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
