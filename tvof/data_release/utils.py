from django.conf import settings
import os
import json


def get_abs_data_path(rel_path, site_key='source'):
    data_release = settings.DATA_RELEASE

    return os.path.join(data_release['sites'][site_key]['path'], rel_path)


def read_settings_file(settings_file_key, default=None, site_key='source'):
    ret = default

    path = get_abs_data_path(
        settings.DATA_RELEASE['settings'][settings_file_key],
        site_key
    )

    if os.path.exists(path):
        with open(path, 'rt') as fh:
            s = fh.read()
        ret = json.loads(s)

    return ret


def write_settings_file(settings_file_key, content, site_key='source'):
    path = get_abs_data_path(
        settings.DATA_RELEASE['settings'][settings_file_key],
        site_key
    )

    with open(path, 'wt') as fh:
        fh.write(json.dumps(content))


def read_text_viewer_filters(client='textviewer', site_key=None):
    ret = None

    filters = read_settings_file('text_viewer_filters', None, site_key)
    if filters:
        ret = filters[client]

    return ret
