from django.apps import AppConfig
from django.conf import settings
from .utils import get_abs_data_path
import os


class DataReleaseConfig(AppConfig):
    name = 'data_release'

    def ready(self):
        self._make_data_release_folders()

    @staticmethod
    def _make_data_release_folders(data_release_site_key='source'):
        '''Creates all the data_release folders.
        In this instance and all its registered targets.'''

        site_keys = settings.DATA_RELEASE_AVAILABLE_TARGETS + ['source']

        data_release = settings.DATA_RELEASE
        for site_key, site_info in data_release['sites'].items():
            if site_key in site_keys:
                for folder in data_release['folders']:
                    path = get_abs_data_path(folder, site_key)
                    print('CREATE ' + path)
                    if not os.path.exists(path):
                        os.makedirs(path)
