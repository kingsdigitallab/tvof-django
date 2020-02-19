from django.views.generic.edit import FormView
from django import forms
from django.urls.base import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from shutil import copy2
import os


class DataReleaseForm(forms.Form):
    name = forms.CharField(required=False)


class DataReleaseView(LoginRequiredMixin, FormView):
    template_name = 'data_release.html'
    form_class = DataReleaseForm
    success_url = None

    def __init__(self, *args, **kwargs):
        self.config = settings.DATA_RELEASE
        for k, v in self.config['sites'].items():
            v['key'] = k

        return super().__init__(*args, **kwargs)

    def get_site_groups(self, is_target=False):
        ret = []

        if is_target:
            site = self.get_selected_target()
        else:
            site = self.get_source_site()

        for group_key, group in self.config['file_groups'].items():
            files = []
            for file_key, afile in self.config['files'].items():
                if afile['group'] == group_key:
                    file = {k: v for k, v in afile.items()}
                    # file.update(afile)
                    file['key'] = file_key
                    file['stats'] = self.get_file_stats(site, file)
                    files.append(file)
            if files:
                group = {
                    'key': group_key,
                    'name': group['name'],
                    'files': files
                }
                ret.append(group)
            print(files)

        return ret

    def get_file_stats(self, site, file):
        ret = 'not found'
        path = os.path.join(site['path'], file['path'])

        print(path)

        if os.path.exists(path):
            from datetime import datetime
            modified = os.path.getmtime(path)
            ret = datetime.utcfromtimestamp(modified)
            ret = ret.strftime('%d/%m/%Y %H:%M:%S')

        return ret

    def get_success_url(self):
        return reverse('data_release')

    def get_source_site(self):
        return self.config['sites']['source']

    def get_selected_target(self):
        '''Returns the target site currently selected by the user'''
        ret = None

        targets = settings.DATA_RELEASE_AVAILABLE_TARGETS
        if targets:
            default = targets[0]
            selected_key = self.request.GET.get('target', default)
            if selected_key in targets:
                ret = self.config['sites'][selected_key]

        return ret

    def form_valid(self, form):
        ret = super().form_valid(form)
        source = self.get_source_site()
        target = self.get_selected_target()

        if ret and source and target:
            for file_key, file in self.config['files'].items():
                ticked = self.request.POST.get(file_key, '')
                if ticked:
                    src = os.path.join(source['path'], file['path'])
                    dst = os.path.join(target['path'], file['path'])
                    # todo: error management
                    copy2(src, dst)

            # todo: restart site

        return ret

    def get_unselected_targets(self):
        selected = self.get_selected_target()

        return [
            self.config['sites'][key]
            for key
            in settings.DATA_RELEASE_AVAILABLE_TARGETS
            if self.config['sites'][key] != selected
        ]

    def get_context_data(self, **kwargs):
        ret = super().get_context_data(**kwargs)

        ret['selected_target'] = self.get_selected_target()
        ret['unselected_targets'] = self.get_unselected_targets()
        ret['source_groups'] = self.get_site_groups()
        ret['target_groups'] = self.get_site_groups(True)

        return ret
