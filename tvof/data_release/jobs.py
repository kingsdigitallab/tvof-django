from django.conf import settings
import time
from datetime import datetime
import os
import signal
from django.core.management import call_command
from subprocess import run, STDOUT

'''
Minimalistic job scheduling system for the text processing tasks.

Supposed to be used in conjunction with a cronjob
and Django management commands (see 'datajob').

All the settings are specified in settings.py DATA_RELEASE['jobs'].

Job status save in kiln_out/jobs/JOBNAME.status
Job execution log saved in kiln_out/jobs/JOBNAME.log
'''

STATUS_SCHEDULED = -1000  # Exception: this is NOT an error!
STATUS_DIED = -1008
STATUS_KILLED = -1009
INVALID_ACTION = -1010
STATUS_INVALID_STATUS_CODE = -1011
STATUS_PYTHON_EXCEPTION = -1012
# Special status for a process running on a remote container / machine
# the actual number = STATUS_RUNNING_REMOTELY - PID
# Unlike same-machine execution we don't use the positive PID,
# because it could be confusing.
# (e.g. test if process died based on that is not correct).
STATUS_RUNNING_REMOTELY = -100000000 # Exception: this is NOT an error!


def job_action(job_key, action, project_root=None):
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
    reset
    '''
    ret = INVALID_ACTION

    if project_root == '':
        return ret

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
            ajob_action = getattr(job, action, None)
            if ajob_action:
                ret = ajob_action()
            else:
                print('ERROR: unknown action {}'.format(action))

    return ret


class Job:
    '''Abstract base class for all Job types.
    Subclasses just have to define the actual job in _run(self)
    '''
    slug = 'unnamed'

    def __init__(self, job_parent=None):
        if job_parent is None:
            job_parent = settings.KILN_STATIC_PATH
        self.job_parent = job_parent

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
        elif status == STATUS_INVALID_STATUS_CODE:
            message = 'error (invalid status code)'
        elif status == STATUS_PYTHON_EXCEPTION:
            message = 'python exception'
        elif status < STATUS_RUNNING_REMOTELY:
            message = 'running (remotely)'
        elif status < 0:
            message = 'unknown error ({})'.format(status)
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

        with open(self.get_job_path('log'), 'wt') as self.run_fh:
            # run the job
            self._log('Start', True)
            try:
                # sys.stdout = fh
                ret = self._run()
                if ret > 0:
                    ret = -ret
            except BaseException as e:
                self._log('EXCEPTION: ({}) {}'.format(
                    e.__class__.__name__, str(e)
                ))
                ret = STATUS_PYTHON_EXCEPTION

            # set new status
            self.set_job_status(ret)
            self._log('Done ({})'.format(ret), True)

        return ret

    def reset(self):
        return self.set_job_status(0)

    # ------------------------------------

    def _log(self, message, show_date=False):
        '''Write a message to the job log'''
        if show_date:
            message += ' {}'.format(datetime.utcnow())
        self.run_fh.write(message + '\n')
        self.run_fh.flush()

    def get_job_path(self, file_type):
        jobs_path = os.path.join(self.job_parent, 'jobs')
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
                ret = STATUS_INVALID_STATUS_CODE

        if ret > 0:
            # still running?
            try:
                os.kill(ret, 0)
            except ProcessLookupError:
                ret = self.set_job_status(STATUS_DIED)
            except PermissionError:
                # www-data may not have permissions to
                # check if pid exists... we just assume its running
                pass

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
        # Used to be False, before dockerisation. As Kiln conversion
        # could be called from the machine as the this django code.
        # We still use this job to schedule conversion. But the actual
        # job should be running from the kiln container.
        in_docker = True
        if in_docker:
            print (
                'With Docker this job is no longer synchronous. '
                'Execution should be initiated from the kiln container.'
            )
            return 2
        else:
            command = settings.DATA_RELEASE['jobs'][self.slug]['command']
            ret = run_shell_command(command, self.run_fh)
            return ret.returncode


class JobIndex(Job):
    slug = 'index'

    def _run(self):
        ret = call_command(
            #'rebuild_index', '--noinput',
            'textsearch', 'ri',
            stdout=self.run_fh, stderr=self.run_fh
        )
        if ret is None:
            # rebuild_index returns None on success
            ret = 0
        return ret


def run_shell_command(command, fh):
    '''runs a shell command and returns a CompletedProcess object
    ret.stdout, ret.returncode
    '''
    ret = run(
        args=command,
        stdout=fh,
        stderr=STDOUT,
        shell=True
    )
    print(ret)
    return ret
