from nose.plugins import Plugin
from nose.failure import Failure
import datetime
import os
import pkg_resources
import subprocess

def _IN_PACKAGE(p):
    return os.path.join(os.path.dirname(__file__), p)

_SUCCESS_ICON = pkg_resources.resource_filename("snort", "success.png")
_FAILURE_ICON = pkg_resources.resource_filename("snort", "failure.png")
_PYTHON_ICON  = pkg_resources.resource_filename("snort", "python.png")

class NosePlugin(Plugin):
    name = 'snort'

    def begin(self):
        self.start_time = datetime.datetime.now()
        self._growl("Starting tests...", "Started at : [{0}]".format(self.start_time.isoformat()))

    def _growl_success(self, title, message):
        return self._growl(title, message, _SUCCESS_ICON)
    def _growl_failure(self, title, message):
        return self._growl(title, message, _FAILURE_ICON)

    def _growl(self, title, message, icon=_PYTHON_ICON, sticky=False):
        cmdline = "growlnotify -t {0}".format(
            _quote(title),
            )
        if icon is not None:
            cmdline += " --image {0}".format(_quote(icon))
        if sticky:
            cmdline += " -s"
        p = subprocess.Popen(cmdline, shell=True, stdin=subprocess.PIPE, close_fds=True)
        p.stdin.write(message)
        p.stdin.close()
        result = p.wait()
        if result != 0:
            raise Exception("growlnotify failed!")
    def addFailure(self, test, (errtype, err, tb), *_):
        self._add_failure_or_error("Failure", test, errtype, err)
    def addError(self, test, (errtype, err, tb), *_):
        self._add_failure_or_error("Error", test, errtype, err)
    def _add_failure_or_error(self, msg, test, errtype, err):
        if isinstance(test, Failure):
            test = "?"
        else:
            test = str(test)
        self._growl_failure("{0} in {1}".format(msg, test),
                      "{0}: {1}".format(errtype.__name__, _truncate_from_end(str(err), _MAX_ERROR_STRING_LENGTH)))
    def finalize(self, result=None):
        """
        Clean up any created database and schema.
        """
        fail_msg = '\n'.join(["Failed: %s" % name for name, ex in result.failures])
        err_msg = '\n'.join(["Error: %s" % name for name, ex in result.errors])

        big_msg = '\n'.join([fail_msg, err_msg])

        self.finish_time = datetime.datetime.now()

        delta = self.finish_time - self.start_time
        endtime_msg = 'Completed in  %s.%s seconds' % (delta.seconds, delta.microseconds)
        if result.wasSuccessful():
            self._growl_success("%s tests run ok" % result.testsRun, endtime_msg)
        else:
            self._growl_failure("%s tests. %s failed, %s errors" % (result.testsRun, len(result.failures), len(result.errors)), endtime_msg)

_MAX_ERROR_STRING_LENGTH = 300

def _truncate_from_end(s, length):
    if len(s) < length:
        return s
    return "{0}...".format(s[:length - 3])

def _quote(s):
    s = s.replace("\\", "\\\\").replace('"', '\\"')
    if " " in s:
        s = '"{0}"'.format(s)
    else:
        s = s.replace("'", "\\'")
    return s

