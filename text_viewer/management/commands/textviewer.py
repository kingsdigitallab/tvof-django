from django.core.management.base import BaseCommand
from text_viewer.kiln_requester import CachedRequesterKiln


class Command(BaseCommand):
    help = 'Toolbox for the Text Viewer app'

    def add_arguments(self, parser):
        parser.add_argument('actions', nargs=1, type=str)

    def handle(self, *args, **options):

        actions = options.get('actions', [])
        action = actions[0]

        known_action = False

        if action == 'test_cache':
            known_action = True
            self.test_cache()

        if not known_action:
            print('ERROR: unknown action "%s"' % action)
        else:
            print('done')

    def test_cache(self):
        import os
        import threading
        import time
        domain = 'http://10.0.2.2:9999'
        # domain = 'http://192.168.101.1:9999'
        wpath = '/backend/texts/Royal/critical/'

        if 0:
            domain = 'http://speedtest.ftp.otenet.gr'
            wpath = '/files/test10Mb.db'

        # domain = 'http://127.0.0.1:9999'

        # TODO: move this to a separate unit test

        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tvof.settings")

        rets = []

        chunk_size = 10
        repetition = 1
        thread_count = 10

        CachedRequesterKiln().clear_disk_cache()

        def task(tid=0):
            cr = CachedRequesterKiln(chunk_size=chunk_size)
            for i in range(repetition):
                ret = cr.request(domain + wpath, False)
                print('%s %s' % (tid, len(ret)))
                rets.append(len(ret))

        # task()
        threads = []
        for i in range(thread_count):
            t = threading.Thread(target=task, args=(i,))
            threads.append(t)
            t.start()
            time.sleep(1)

        while threads:
            threads = [at for at in threads if at.is_alive()]
            time.sleep(1)

        rets = set(rets)
        if len(rets) > 1:
            print('TEST FAILED: all responses should have the same length, ' +
                  'we have %s' % repr(rets))
