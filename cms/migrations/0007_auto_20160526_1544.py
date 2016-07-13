# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-26 14:44
from __future__ import unicode_literals

import cms.models
from django.db import migrations
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0006_auto_20160518_1259'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='content',
            field=wagtail.wagtailcore.fields.StreamField([(b'paragraph', wagtail.wagtailcore.blocks.RichTextBlock())], default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='content',
            field=wagtail.wagtailcore.fields.StreamField([(b'heading', wagtail.wagtailcore.blocks.CharBlock(classname=b'')), (b'paragraph', wagtail.wagtailcore.blocks.RichTextBlock()), (b'image', wagtail.wagtailimages.blocks.ImageChooserBlock()), (b'image_caption', wagtail.wagtailcore.blocks.CharBlock(classname=b'richtext-caption')), (b'image_and_caption', wagtail.wagtailcore.blocks.StructBlock([(b'images', wagtail.wagtailimages.blocks.ImageChooserBlock()), (b'caption', wagtail.wagtailcore.blocks.RichTextBlock())])), (b'image_and_text', wagtail.wagtailcore.blocks.StructBlock([(b'text', wagtail.wagtailcore.blocks.RichTextBlock()), (b'image', wagtail.wagtailimages.blocks.ImageChooserBlock()), (b'caption', wagtail.wagtailcore.blocks.RichTextBlock()), (b'alignment', cms.models.ImageFormatChoiceBlock())]))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='indexpage',
            name='content',
            field=wagtail.wagtailcore.fields.StreamField([(b'heading', wagtail.wagtailcore.blocks.CharBlock(classname=b'')), (b'paragraph', wagtail.wagtailcore.blocks.RichTextBlock()), (b'image', wagtail.wagtailimages.blocks.ImageChooserBlock()), (b'image_caption', wagtail.wagtailcore.blocks.CharBlock(classname=b'richtext-caption')), (b'image_and_caption', wagtail.wagtailcore.blocks.StructBlock([(b'images', wagtail.wagtailimages.blocks.ImageChooserBlock()), (b'caption', wagtail.wagtailcore.blocks.RichTextBlock())])), (b'image_and_text', wagtail.wagtailcore.blocks.StructBlock([(b'text', wagtail.wagtailcore.blocks.RichTextBlock()), (b'image', wagtail.wagtailimages.blocks.ImageChooserBlock()), (b'caption', wagtail.wagtailcore.blocks.RichTextBlock()), (b'alignment', cms.models.ImageFormatChoiceBlock())]))]),
        ),
        migrations.AlterField(
            model_name='richtextpage',
            name='content',
            field=wagtail.wagtailcore.fields.StreamField([(b'heading', wagtail.wagtailcore.blocks.CharBlock(classname=b'')), (b'paragraph', wagtail.wagtailcore.blocks.RichTextBlock()), (b'image', wagtail.wagtailimages.blocks.ImageChooserBlock()), (b'image_caption', wagtail.wagtailcore.blocks.CharBlock(classname=b'richtext-caption')), (b'image_and_caption', wagtail.wagtailcore.blocks.StructBlock([(b'images', wagtail.wagtailimages.blocks.ImageChooserBlock()), (b'caption', wagtail.wagtailcore.blocks.RichTextBlock())])), (b'image_and_text', wagtail.wagtailcore.blocks.StructBlock([(b'text', wagtail.wagtailcore.blocks.RichTextBlock()), (b'image', wagtail.wagtailimages.blocks.ImageChooserBlock()), (b'caption', wagtail.wagtailcore.blocks.RichTextBlock()), (b'alignment', cms.models.ImageFormatChoiceBlock())]))]),
        ),
    ]
