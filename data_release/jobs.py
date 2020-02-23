from django.conf import settings
import time
from datetime import datetime
import os
import signal
from django.core.management import call_command
from subprocess import PIPE, run

STATUS_SCHEDULED = -1000  # Exception: this is NOT an error!
STATUS_DIED = -1008
STATUS_KILLED = -1009
INVALID_ACTION = -1010


def job_action(job_key, action='', project_root=''):
    '''
    A facade for the JobX classes.

    The action directly refers to the method of the same name on
    the Job class.

    Possible action:

    run
    schedule
    unschedule
    run_if_scheduled
    kill
    status
    info
    log
    '''
    ret = INVALID_ACTION

    job_info = settings.DATA_RELEASE['jobs'].get(job_key, None)

    if not job_info:
        print(
            '''ERROR: unknown job "{}", see settings.DATA_RELASE['jobs']'''.format(
                job_key)
        )
    else:
        job_class_name = job_info['class_name']
        job_class = globals().get(job_class_name, None)
        if job_class is None:
            print('ERROR: unknown job class name "{}"'.format(job_class_name))
        else:
            job = job_class(project_root)
            job_action = getattr(job, action, None)
            if job_action:
                ret = job_action()
            else:
                print('ERROR: unknown action {}'.format(action))

    return ret


class Job:
    slug = 'unnamed'

    def __init__(self, project_root):
        self.project_root = project_root

    def log(self):
        '''return the content of current/last execution log'''
        ret = ''
        status_path = self.get_job_path('log')
        if os.path.exists(status_path):
            with open(status_path, 'rt') as fh:
                ret = fh.read()
        return ret

    def info(self):
        '''returns dictionary with metadata about the job'''

        status = self.get_job_status()
        message = 'not running'

        if status == STATUS_SCHEDULED:
            message = 'scheduled'
        elif status == STATUS_DIED:
            message = 'died'
        elif status == STATUS_KILLED:
            message = 'interrupted'
        elif status < 0:
            message = 'unknown error'
        elif status > 0:
            message = 'running'

        modified = None

        status_path = self.get_job_path('status')
        if os.path.exists(status_path):
            modified = datetime.fromtimestamp(os.path.getmtime(status_path))

        return {
            'status': status,
            'message': message,
            'modified': modified
        }

    def kill(self):
        '''kill a running job'''
        ret = 0

        pid = self.get_job_status()
        if pid > 0:
            try:
                os.kill(pid, signal.SIGKILL)
                self.set_job_status(STATUS_KILLED)
            except ProcessLookupError:
                ret = 0

        return ret

    def status(self):
        '''show status code (>0 = PID, <0 error or scheduling)'''
        return self.get_job_status()

    def schedule(self):
        '''schedule a job for later execution'''
        ret = self.get_job_status()
        if ret < 1:
            ret = self.set_job_status(STATUS_SCHEDULED)
        return ret

    def unschedule(self):
        '''unschedule a job if it is scheduled (otherwise do nothing)'''
        ret = self.get_job_status()
        if ret == STATUS_SCHEDULED:
            ret = self.set_job_status(0)
        return ret

    def run_if_scheduled(self):
        '''run the job immediately if it is scheduled'''
        ret = 0
        status = self.get_job_status()
        if status == STATUS_SCHEDULED:
            ret = self.run()

        return ret

    def run(self):
        '''run a job immediately (unless it's already running)'''
        ret = self.get_job_status()
        if ret > 0:
            return ret

        # set running status
        self.set_job_status(os.getpid())

        import sys
        # sysout = sys.stdout
        self.run_fh = None

        try:
            self.run_fh = open(self.get_job_path('log'), 'w')
            self.run_fh.write('start')
            # sys.stdout = fh

            # run the job
            ret = self._run()
            if ret > 0:
                ret = -ret
        finally:
            if self.run_fh:
                self.run_fh.close()
            # sys.stdout = sysout
            # raise e

        # set new status
        self.set_job_status(ret)

        return ret

    def get_job_path(self, file_type):
        jobs_path = os.path.join(self.project_root, 'kiln_out', 'jobs')
        if not os.path.exists(jobs_path):
            os.makedirs(jobs_path)

        ret = os.path.join(jobs_path, self.slug + '.' + file_type)
        # print(ret)
        return ret

    def set_job_status(self, status):
        status_path = self.get_job_path('status')
        with open(status_path, 'w') as fh:
            fh.write(str(status))
        return status

    def get_job_status(self):
        '''
        0: never run or last run completed successfully
        >0: this process ID
        STATUS_SCHEDULED: STATUS_SCHEDULED
        <0: error code of the last run job
        '''
        ret = 0
        status_path = self.get_job_path('status')
        if os.path.exists(status_path):
            with open(status_path, 'rt') as fh:
                ret = fh.read()
            try:
                ret = int(ret)
            except:
                pass

        if ret > 0:
            # still running?
            try:
                os.kill(ret, 0)
            except ProcessLookupError:
                ret = self.set_job_status(STATUS_DIED)

        return ret


class JobTest(Job):
    slug = 'test'

    def _run(self):
        ret = 0
        print('TEST')
        time.sleep(20)
        print('TEST-END')
        return ret


class JobConvert(Job):
    slug = 'convert'

    def _run(self):
        command = settings.DATA_RELEASE['jobs'][self.slug]['command']
        ret = os.system(command)
        return ret


class JobIndex(Job):
    slug = 'index'

    def _run(self):
        ret = call_command(
            'rebuild_index', '--noinput',
            stdout=self.run_fh, stderr=self.run_fh
        )
        return ret


def run_shell_command(command):
    '''runs a shell command and returns a CompletedProcess object
    ret.stdout, ret.returncode
    '''
    ret = run(
        args=command,
        stdout=PIPE,
        stderr=PIPE,
        shell=True
    )
    return ret
