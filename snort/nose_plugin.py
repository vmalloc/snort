from .generic_plugin import GenericPlugin
from nose.plugins import Plugin as NosePluginBase
from nose.failure import Failure

class NosePlugin(NosePluginBase, GenericPlugin):
    name = 'snort'

    def begin(self):
        self._begin_run()

    def addFailure(self, test, exception_tuple, *_):
        self._add_failure(self._get_test_name(test), exception_tuple)
    def addError(self, test, exception_tuple, *_):
        self._add_error(self._get_test_name(test), exception_tuple)
    def _get_test_name(self, test):
        if isinstance(test, Failure):
            return "?"
        return str(test)
    def finalize(self, result=None):
        self._end_run(result)

