# -*- coding: utf-8 -*-


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
    location = models.CharField(
        max_length=20,
        help_text='location id for the seg comprising this token'
    )
    token_number = models.IntegerField(
        help_text='The sequential index of the token relative to the seg'
    )
    pos = models.CharField(max_length=30, help_text='part of speech')

    # these fields are derived from .location
    manuscript = models.CharField(max_length=30, default='unspecified')
    section_name = models.CharField(max_length=100, default='unspecified')
    is_rubric = models.BooleanField(default=False)

    @classmethod
    def update_or_create_from_kwik_item(cls, item, token):
        data = cls._get_data_from_kwik_item(item, token)

        ret, _ = cls.objects.update_or_create(
            location=data['location'],
            token_number=data['token_number'],
            defaults=data
        )

        return ret

    @classmethod
    def create_from_kwik_item(cls, item, token):
        ret = AnnotatedToken(**cls._get_data_from_kwik_item(item, token))
        ret.save()

        return ret

    @classmethod
    def _get_data_from_kwik_item(cls, item, token):
        data = {
            k: (v or 'unspecified')
            for k, v
            in list(item.attrib.items())
            if k not in ['type', 'n']
        }
        location_parts = data['location'].split('_')

        ret = dict(
            token=token,
            token_number=item.attrib['n'],
            manuscript=location_parts[0],
            section_name='section X',
            is_rubric=(len(location_parts) < 3),
            ** data
        )

        return ret
