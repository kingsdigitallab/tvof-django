# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-26 15:17


from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0007_auto_20160526_1544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='content',
            field=wagtail.core.fields.StreamField([(b'paragraph', wagtail.core.blocks.RichTextBlock()), (b'image_and_caption', wagtail.core.blocks.StructBlock([(b'images', wagtail.images.blocks.ImageChooserBlock()), (b'caption', wagtail.core.blocks.RichTextBlock())]))]),
        ),
    ]
