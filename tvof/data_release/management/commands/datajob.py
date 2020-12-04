'''
'''

from django.core.management.base import BaseCommand, DjangoHelpFormatter
from ...jobs import job_action, INVALID_ACTION
from django.conf import settings


class Command(BaseCommand):
    help = 'TVOF Data processing job'

    def add_arguments(self, parser):

        jobs = settings.DATA_RELEASE['jobs']

        choices = jobs.keys()

        parser.add_argument(
            'jobname', nargs=1, type=str,
            choices=choices,
            metavar='jobname',
            help='|'.join(choices),
        )

        choices = ['run', 'schedule', 'run_if_scheduled',
                   'unschedule', 'kill', 'status', 'info', 'log', 'reset']

        parser.add_argument(
            'action', nargs=1, type=str,
            choices=choices,
            metavar='action',
            help='|'.join(choices),
        )

    def handle(self, *args, **options):
        self.options = options
        self.jobname = options['jobname'][0]
        self.action = options['action'][0]

        res = job_action(self.jobname, self.action)
        return str(res)
