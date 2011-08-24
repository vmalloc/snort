import datetime
import os
import pkg_resources
import subprocess

_SUCCESS_ICON = pkg_resources.resource_filename("snort", "success.png")
_FAILURE_ICON = pkg_resources.resource_filename("snort", "failure.png")
_SKIP_ICON    = pkg_resources.resource_filename("snort", "skip.png")
_PYTHON_ICON  = pkg_resources.resource_filename("snort", "python.png")

class GenericPlugin(object):
    def _begin_run(self):
        self._start_time = datetime.datetime.now()
        self._growl("Starting tests...", "Started at : [{0}]".format(self._start_time.isoformat()))
    def _add_failure(self, test_name, exception_tuple):
        self._add_failure_or_error("Failure", test_name, exception_tuple)
    def _add_error(self, test_name, exception_tuple):
        self._add_failure_or_error("Error", test_name, exception_tuple)
    def _add_failure_or_error(self, msg, test_name, exception_tuple):
        errtype, err, tb = exception_tuple
        self._growl_failure("{0} in {1}".format(msg, test_name),
                      "{0}: {1}".format(errtype.__name__, _truncate_from_end(str(err), _MAX_ERROR_STRING_LENGTH)))
    def _end_run(self, result):
        fail_msg = '\n'.join(["Failed: %s" % name for name, ex in result.failures])
        err_msg = '\n'.join(["Error: %s" % name for name, ex in result.errors])

        big_msg = '\n'.join([fail_msg, err_msg])

        self._finish_time = datetime.datetime.now()

        delta = self._finish_time - self._start_time
        endtime_msg = 'Completed in  %s.%s seconds' % (delta.seconds, delta.microseconds)
        if result.wasSuccessful():
            msg = "{0} tests run ok.".format(result.testsRun - len(result.skipped))
            if result.skipped:
                msg += " {0} skipped.".format(len(result.skipped))
                func = self._growl_skip
            else:
                func = self._growl_success
            func(msg, endtime_msg)
        else:
            self._growl_failure("%s tests. %s failed, %s errors" % (result.testsRun, len(result.failures), len(result.errors)), endtime_msg)


    def _growl_success(self, title, message):
        return self._growl(title, message, _SUCCESS_ICON)
    def _growl_skip(self, title, message):
        return self._growl(title, message, _SKIP_ICON)
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
        p.stdin.write(message.encode('utf-8'))
        p.stdin.close()
        result = p.wait()
        if result != 0:
            raise Exception("growlnotify failed!")


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

