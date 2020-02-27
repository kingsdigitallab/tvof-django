from django.views.generic.edit import FormView
from django import forms
from django.urls.base import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from shutil import copy2
import os
from .jobs import job_action, STATUS_SCHEDULED
from django.views.generic.base import TemplateView


class DataReleaseForm(forms.Form):
    index_input_file = forms.FileField(required=False)


class DataReleaseView(LoginRequiredMixin, FormView):
    template_name = 'data_release.html'
    form_class = DataReleaseForm
    success_url = None

    def __init__(self, *args, **kwargs):
        self.config = settings.DATA_RELEASE
        self.errors = []
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
                job_slug = group['job']

                group_dict = {
                    'key': group_key,
                    'name': group['name'],
                    'files': files,
                    'job': self.config['jobs'][job_slug].copy(),
                }

                group_dict['job']['slug'] = job_slug

                group_dict['job']['info'] = job_action(
                    job_slug,
                    'info',
                    site['path']
                )

                print(group_dict['job'])

                job_status = group_dict['job']['info']['status']
                class_css = ''
                if job_status > 0:
                    self.running_or_scheduled_job_count += 1
                    class_css = 'job-running'
                elif job_status == STATUS_SCHEDULED:
                    self.running_or_scheduled_job_count += 1
                    class_css = 'job-scheduled'
                elif job_status != 0:
                    class_css = 'job-error'
                group_dict['job']['class'] = class_css

                ret.append(group_dict)

        return ret

    def get_file_stats(self, site, file):
        ret = 'not found'
        path = os.path.join(site['path'], file['path'])

        if os.path.exists(path):
            from datetime import datetime
            modified = os.path.getmtime(path)
            ret = datetime.utcfromtimestamp(modified)
            ret = ret.strftime('%d %b %Y, %H:%M:%S')

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
            self.process_index_input_file()

            search_file_copied = False

            for file_key, file in self.config['files'].items():
                ticked = self.request.POST.get(file_key, '')
                if ticked:
                    src = os.path.join(source['path'], file['path'])
                    dst = os.path.join(target['path'], file['path'])
                    # TODO: error management
                    copy2(src, dst)

                    if file['group'] == 'search':
                        search_file_copied = True

            if search_file_copied:
                job_action('index', 'schedule', target['path'])

        return ret

    def process_index_input_file(self):
        index_input_file = self.request.FILES.get('index_input_file', None)
        if not index_input_file:
            return

        # write the file to disk
        upload_path = os.path.join(settings.MEDIA_UPLOAD_DIR, 'search.zip')
        with open(upload_path, 'wb+') as destination:
            for chunk in index_input_file.chunks():
                destination.write(chunk)

        import zipfile
        # unzip it
        unzip_path = settings.MEDIA_UPLOAD_DIR
        with zipfile.ZipFile(upload_path, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)

            # move and rename the files to kiln_out
            file_names = zip_ref.namelist()

            #
            patterns = {
                r'fr': 'prepared/fr_tokenised.xml',
                r'royal': 'prepared/royal_tokenised.xml',
                r'kwic': 'received/kwic-out.xml'
            }
            if len(file_names) != 3:
                self.add_error(
                    'zip file should contain three files exactly'
                )
            else:
                import re
                for file_name in file_names:
                    recognised = False
                    for pattern, new_name in patterns.items():
                        if re.search(r'(?i)' + re.escape(pattern), file_name):
                            # print(file_name, new_name)
                            os.replace(
                                os.path.join(unzip_path, file_name),
                                os.path.join(
                                    settings.KILN_STATIC_PATH, new_name
                                )
                            )
                            recognised = True
                    if not recognised:
                        self.add_error(
                            '{} is not a recognised file name.'.format(
                                file_name
                            ))
                        break

                if recognised:
                    # schedule the indexing
                    job_action('index', 'schedule', settings.BASE_DIR)

    def add_error(self, message):
        from django.contrib import messages
        messages.error(self.request, message)

    def get_errors(self):
        return self.errors

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

        self.running_or_scheduled_job_count = 0

        ret['selected_target'] = self.get_selected_target()
        ret['unselected_targets'] = self.get_unselected_targets()
        ret['source_groups'] = self.get_site_groups()
        ret['target_groups'] = self.get_site_groups(True)
        ret['editable'] = \
            self.running_or_scheduled_job_count == 0
        print('sch-running-count', self.running_or_scheduled_job_count)

        ret['errors'] = self.get_errors()

        return ret


class DataReleaseJobView(LoginRequiredMixin, TemplateView):
    template_name = 'data_release_job.html'

    def get_context_data(self, **kwargs):
        ret = super().get_context_data(**kwargs)

        site_key = kwargs['site']
        site_dict = settings.DATA_RELEASE['sites'].get(site_key, {})

        ret['site'] = site_dict

        if site_dict:
            job_key = kwargs['job']

            job_dict = settings.DATA_RELEASE['jobs'].get(job_key, {})

            ret['job'] = job_dict.copy()
            ret['job'].update({
                'log': job_action(job_key, 'log', site_dict['path']),
                'info': job_action(job_key, 'info', site_dict['path']),
            })

        return ret
