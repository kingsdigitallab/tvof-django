# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class AnnotatedToken(models.Model):
    '''
    Model for an entry in a Kwic received from Lemmings.
    The only reason to have it in the DB is that it is required by
    django-haystack.
    This is however not scalable and a huge waste of resources.

    TODO: we should instead keep the data in the XML and index it directly
    from there rather than have a duplicated copy in the database.

    TODO: create lemma, token and pos models? only benefit here is
    space savings.

    <kwiclist>
      <sublist key="·c·">
        <item type="seg_item" location="edfr20125_00598_08" n="23"
            preceding="chargees , ele lor envoia ·xx· bues et"
            following="pors et ·c· moutons cras et autant"
            lemma="cent">
          <string>·c·</string>
        </item>

    '''
    token = models.CharField(max_length=30)
    preceding = models.CharField(max_length=200)
    following = models.CharField(max_length=200)
    lemma = models.CharField(max_length=30)
    location = models.CharField(max_length=20)
    token_number = models.IntegerField(
        help_text='The sequential index of the token relative to the seg'
    )
    pos = models.CharField(max_length=30)
