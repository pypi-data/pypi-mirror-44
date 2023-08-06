import functools
from aiohttp.helpers import AccessLogger, KeyMethod


class AGIAccessLogger(AccessLogger):
    LOG_FORMAT = '%a - %t (%D) "%r" %s %b'

    def compile_format(self, log_format):
        """Translate log_format into form usable by modulo formatting

        All known atoms will be replaced with %s
        Also methods for formatting of those atoms will be added to
        _methods in apropriate order

        For example we have log_format = "%a %t"
        This format will be translated to "%s %s"
        Also contents of _methods will be
        [self._format_a, self._format_t]
        These method will be called and results will be passed
        to translated string format.

        Each _format_* method receive 'args' which is list of arguments
        given to self.log

        Exceptions are _format_e, _format_i and _format_o methods which
        also receive key name (by functools.partial)

        """
        # list of (key, method) tuples, we don't use an OrderedDict as users
        # can repeat the same key more than once
        methods = list()

        for atom in self.FORMAT_RE.findall(log_format):
            if atom[1] == '':
                format_key = self.LOG_FORMAT_MAP[atom[0]]
                m = getattr(self, '_format_%s' % atom[0])
            else:
                format_key = (self.LOG_FORMAT_MAP[atom[2]], atom[1])
                m = getattr(self, '_format_%s' % atom[2])
                m = functools.partial(m, atom[1])

            methods.append(KeyMethod(format_key, m))

        log_format = self.FORMAT_RE.sub(r'%s', log_format)
        log_format = self.CLEANUP_RE.sub(r'%\1', log_format)
        return log_format, methods

    @staticmethod
    def _format_r(request, response, time):
        return '{} {}'.format(request.method, request.path_qs)
