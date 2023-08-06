import re

import typing
from itertools import zip_longest

import yarl
import collections
from enum import IntEnum

from aioagi.log import agi_server_logger, agi_client_logger
from aioagi.commands import AGICommand
from aioagi.exceptions import AGIAppError

AGIRequestMessage = collections.namedtuple(
    'AGIRequestMessage',
    ['method', 'path', 'headers', 'url']
)


class AGICode(IntEnum):
    TRYING = 100

    OK = 200

    MEMORY_ALLOCATION_FAILURE = 503
    INVALID_COMMAND = 510
    COMMAND_NOT_PERMITTED = 511
    INVALID_COMMAND_SYNTAX = 520

    # Internal codes
    UNKNOWN = 1000


class AGIMessage:
    def __init__(self, status: AGICode, result: str, data: dict, info: str = ''):
        self.status = status
        self.result = result
        self.data = data
        self.info = info

    def __repr__(self):
        return '{class_name}(status={status}, result={result}, data={data}, info="{info}")'.format(
            class_name=self.__class__.__name__,
            status=self.status,
            result=self.result,
            data=self.data,
            info=self.info,
        )

    def result_as_char(self):
        if self.result == '0':
            return ''

        try:
            return chr(int(self.result))
        except (TypeError, ValueError):
            raise AGIAppError(message='Unable to convert result to char: {}'.format(self.result))

    def result_as_int(self):
        try:
            return int(self.result)
        except (TypeError, ValueError):
            raise AGIAppError(message='Unable to convert result to int: {}'.format(self.result))

    def result_as_bool(self):
        try:
            return bool(int(self.result))
        except (TypeError, ValueError):
            raise AGIAppError(message='Unable to convert result to int: {}'.format(self.result))

    def result_to_char(self):
        self.result = self.result_as_char()
        return self

    def result_to_int(self):
        self.result = self.result_as_int()
        return self

    def result_to_bool(self):
        self.result = self.result_as_bool()
        return self

    def as_data(self):
        result = ' result={}'.format(self.result) if self.result is not None else ''
        data = ' ({data})'.format(data=self.data.pop('data')) if 'data' in self.data else ''

        key_value = ['{}={}'.format(key, value) for key, value in self.data.items() if key != 'data']
        key_value = ' {}'.format(key_value) if key_value else ''

        return '{status}{result}{data}{key_value}\n'.format(
            status=self.status,
            result=result,
            data=data,
            key_value=key_value,
            info=' {}'.format(self.info) if self.info else ''
        )


class AGIClientMessage:
    def __init__(self, command: AGICommand, args):
        self.command = command
        self.args = args

    def __repr__(self):
        return '{class_name}(command={command}, args={args})'.format(
            class_name=self.__class__.__name__,
            command=self.command,
            args=self.args,
        )


class AGIRequestParser:
    method_p = re.compile('[^a-zA-Z0-9_]')

    def __init__(self, protocol, loop):
        self.protocol = protocol
        self.loop = loop

        self._tail = b''
        self._lines = []

    def feed_data(self, data, sep=b'\n', empty=b''):
        message = None
        if self._tail:
            data, self._tail = self._tail + data, empty

        data_len = len(data)
        start_pos = 0

        while start_pos < data_len:
            pos = data.find(sep, start_pos)
            if pos >= start_pos:
                # line found
                self._lines.append(data[start_pos:pos])
                start_pos = pos + 1
                if self._lines[-1] == empty:
                    try:
                        message = self.parse_message(self._lines[:-1])
                    finally:
                        self._lines.clear()

                    break

            else:
                self._tail = data[start_pos:]
                break

        return message

    def parse_message(self, lines):
        """
        Raw protocol:
            agi_network: yes
            agi_network_script: agi/
            agi_request: agi://10.99.99.55:8080/agi/
            agi_channel: SIP/95000-00000005
            agi_language: ru
            agi_type: SIP
            agi_uniqueid: 1502266948.5
            agi_version: 11.14.2
            agi_callerid: 95000
            agi_calleridname: test
            agi_callingpres: 0
            agi_callingani2: 0
            agi_callington: 0
            agi_callingtns: 0
            agi_dnid: 770
            agi_rdnis: unknown
            agi_context: from-internal
            agi_extension: 770
            agi_priority: 2
            agi_enhanced: 0.0
            agi_accountcode:
            agi_threadid: 139689736754944

        headers = {
            'agi_network': 'yes',
            'agi_network_script': 'agi/',
            'agi_request': 'agi://10.99.99.55:8080/agi/',
            'agi_channel': 'SIP/95000-00000005',
            'agi_language': 'ru',
            'agi_type': 'SIP',
            'agi_uniqueid': '1502266948.5',
            'agi_version': '11.14.2',
            'agi_callerid': '95000',
            'agi_calleridname': 'test',
            'agi_callingpres': '0',
            'agi_callingani2': '0',
            'agi_callington': '0',
            'agi_callingtns': '0',
            'agi_dnid': '770',
            'agi_rdnis': 'unknown',
            'agi_context': 'from-internal',
            'agi_extension': '770',
            'agi_priority': '2',
            'agi_enhanced': '0.0',
            'agi_accountcode': '',
            'agi_threadid': '139689736754944',
        }
        """
        headers = collections.OrderedDict([line.decode().split(': ', 1) for line in lines])
        path = headers.get('agi_request', '')

        method = headers.get('agi_type', 'GET').replace(' ', '_').replace('-', '_')
        method = self.method_p.sub('', method).upper()

        return AGIRequestMessage(method, path, headers, yarl.URL(path))


class AGIPayloadParser:
    """
    Parse AGI results.
    """
    status_p = re.compile(r'(?P<status>^\d*)(\s|-)*(?P<response>.*)', re.DOTALL)
    kwargs_p = re.compile(r'(?P<key>\w+)=(?P<value>[^\s]*)')
    data_p = re.compile(r'result=[^\s]+\s*\((?P<data>.*?)\)')

    def __init__(self, payload):
        self.payload = payload
        self._tail = b''

    def feed_eof(self):
        self.payload.feed_eof()

    def feed_data(self, data, sep=b'\n'):
        if self._tail:
            data, self._tail = self._tail + data, b''

        start_pos = 0
        data_len = len(data)

        lines = []
        while start_pos < data_len:
            pos = data.find(sep, start_pos)
            if pos >= start_pos:
                line = data[start_pos:pos]
                lines.append(line)
                start_pos = pos + 1

            else:
                self._tail = data[start_pos:]
                break

        if not lines:
            return False, self._tail

        eof, message, tail = self.parse_message(lines)

        if eof:
            self.payload.feed_eof()

        elif message:
            self.payload.feed_data(message, len(data[:start_pos]))

        elif tail:
            self._tail = tail

        return eof, self._tail

    def parse_message(self, lines):
        """
        AGI Result examples::

            100 result=0 Trying...
            ?
            200 result=0 Gosub complete
            ?
            200 result=%d Gosub failed

            200 result=-1 Gosub label not found"

            200 result=0

            200 result=0 endpos=24807

            200 result=49 endpos=8640

            200 result=-1

            200 result=132456

            200 result=1 (testvariable)

            200 result= (timeout)

            503 result=-2 Memory allocation failure

            510 Invalid or unknown command

            511 Command Not Permitted on a dead channel or intercept routine

            # GET DATA
            520-Invalid command syntax. Proper usage follows:
            Stream the given <replaceable>file</replaceable>, and receive DTMF data.
            Returns the digits received from the channel at the other end.520 End of proper usage.

            HANGUP

        From source code example:
            'ast_agi_send(agi->fd, chan, "%d %s\n", resultcode, ami_res);',
            'ast_agi_send(agi->fd, chan, "%s\n", c->usage);',
            'ast_agi_send(agi->fd, chan, "100 result=0 Trying...\n");',
            'ast_agi_send(agi->fd, chan, "200 result=%c\n", num_deleted > 0 ? \'0\' : \'1\');',
            'ast_agi_send(agi->fd, chan, "200 result=%c\n", res ? \'0\' : \'1\');',
            'ast_agi_send(agi->fd, chan, "200 result=%d (dtmf) endpos=%ld\n", f->subclass.integer, sample_offset);',
            'ast_agi_send(agi->fd, chan, "200 result=%d (hangup) endpos=%ld\n", -1, sample_offset);',
            'ast_agi_send(agi->fd, chan, "200 result=%d (hangup)\n", res);',
            'ast_agi_send(agi->fd, chan, "200 result=%d (randomerror) endpos=%ld\n", res, sample_offset);',
            'ast_agi_send(agi->fd, chan, "200 result=%d (timeout) endpos=%ld\n", res, sample_offset);',
            'ast_agi_send(agi->fd, chan, "200 result=%d (timeout)\n", res);',
            'ast_agi_send(agi->fd, chan, "200 result=%d (waitfor) endpos=%ld\n", res,sample_offset);',
            'ast_agi_send(agi->fd, chan, "200 result=%d (writefile)\n", res);',
            'ast_agi_send(agi->fd, chan, "200 result=%d Gosub failed\n", res);',
            'ast_agi_send(agi->fd, chan, "200 result=%d endpos=%ld\n", res, offsetms);',
            'ast_agi_send(agi->fd, chan, "200 result=%d endpos=%ld\n", res, sample_offset);',
            'ast_agi_send(agi->fd, chan, "200 result=%d\n", res);',
            'ast_agi_send(agi->fd, chan, "200 result=%s (timeout)\n", data);',
            'ast_agi_send(agi->fd, chan, "200 result=%s\n", data);',
            'ast_agi_send(agi->fd, chan, "200 result=%u\n", ast_channel_state(chan));',
            'ast_agi_send(agi->fd, chan, "200 result=%u\n", snapshot->state);',
            'ast_agi_send(agi->fd, chan, "200 result=-1 Gosub label not found\n");',
            'ast_agi_send(agi->fd, chan, "200 result=-1 endpos=%ld\n", sample_offset);',
            'ast_agi_send(agi->fd, chan, "200 result=-1\n");',
            'ast_agi_send(agi->fd, chan, "200 result=0 endpos=%ld\n", current_offset);',
            'ast_agi_send(agi->fd, chan, "200 result=0\n");',
            'ast_agi_send(agi->fd, chan, "200 result=1 (%s) endpos=%ld\n", reason, current_offset);',
            'ast_agi_send(agi->fd, chan, "200 result=1 (%s)\n", ast_str_buffer(buf));',
            'ast_agi_send(agi->fd, chan, "200 result=1 (%s)\n", ast_str_buffer(str));',
            'ast_agi_send(agi->fd, chan, "200 result=1 (%s)\n", buf);',
            'ast_agi_send(agi->fd, chan, "200 result=1 (%s)\n", ret);',
            'ast_agi_send(agi->fd, chan, "200 result=1 (digit) digit=%c endpos=%ld\n", dtmf, current_offset);',
            'ast_agi_send(agi->fd, chan, "200 result=1 (speech) endpos=%ld results=%d %s\n", current_offset, i, tmp);',
            'ast_agi_send(agi->fd, chan, "200 result=1\n");',
            'ast_agi_send(agi->fd, chan, "503 result=-2 Memory allocation failure\n");',
            'ast_agi_send(agi->fd, chan, "520 End of proper usage.\n");',
            'ast_agi_send(agi->fd, chan, "520 Invalid command syntax.  Proper usage not available.\n");',
            'ast_agi_send(agi->fd, chan, "520-Invalid command syntax.  Proper usage follows:\n");',
            'ast_agi_send(agi->fd, chan, "HANGUP\n");',
            'ast_agi_send(fd, chan, "\n");',
            'ast_agi_send(fd, chan,
                "agi_accountcode: %s\n", ast_channel_accountcode(chan) ? ast_channel_accountcode(chan) : "");',
            'ast_agi_send(fd, chan, "agi_arg_%d: %s\n", count, argv[count]);',
            'ast_agi_send(fd, chan, "agi_callingani2: %d\n", ast_channel_caller(chan)->ani2);',
            'ast_agi_send(fd, chan, "agi_callingtns: %d\n", ast_channel_dialed(chan)->transit_network_select);',
            'ast_agi_send(fd, chan, "agi_callington: %d\n", ast_channel_caller(chan)->id.number.plan);',
            'ast_agi_send(fd, chan, "agi_channel: %s\n", ast_channel_name(chan));',
            'ast_agi_send(fd, chan, "agi_context: %s\n", ast_channel_context(chan));',
            'ast_agi_send(fd, chan, "agi_dnid: %s\n", S_OR(ast_channel_dialed(chan)->number.str, "unknown"));',
            'ast_agi_send(fd, chan, "agi_enhanced: %s\n", enhanced ? "1.0" : "0.0");',
            'ast_agi_send(fd, chan, "agi_extension: %s\n", ast_channel_exten(chan));',
            'ast_agi_send(fd, chan, "agi_language: %s\n", ast_channel_language(chan));',
            'ast_agi_send(fd, chan, "agi_priority: %d\n", ast_channel_priority(chan));',
            'ast_agi_send(fd, chan, "agi_request: %s\n", request);',
            'ast_agi_send(fd, chan, "agi_threadid: %ld\n", (long)pthread_self());',
            'ast_agi_send(fd, chan, "agi_type: %s\n", ast_channel_tech(chan)->type);',
            'ast_agi_send(fd, chan, "agi_uniqueid: %s\n", ast_channel_uniqueid(chan));',
            'ast_agi_send(fd, chan, "agi_version: %s\n", ast_get_version());',
            'ast_agi_send(s, NULL, "agi_network_script: %s\n", script);',
            'ast_agi_send;'
        """
        message = b'\n'.join(lines).decode()
        if AGICommand.HANGUP in message:
            return True, None, None

        result = None
        match = self.status_p.search(message)
        if match:
            data = match.groupdict()
            message_data = {}
            status_int = int(data['status'])
            try:
                status = AGICode(status_int)
            except ValueError:
                status = AGICode.UNKNOWN
                message_data['_status'] = status_int
                message_data['_message'] = message
                agi_server_logger.warning('Unhandled code or undefined response: %s', status)

            info = self.kwargs_p.sub('', self.data_p.sub('', data['response'])).strip()

            if status == AGICode.OK:
                for key, value in self.kwargs_p.findall(data['response']):
                    if key == 'result':
                        result = value
                    else:
                        message_data[key] = value

                data_match = self.data_p.search(data['response'])
                if data_match:
                    message_data['data'] = data_match.group(1)

            elif status == AGICode.INVALID_COMMAND_SYNTAX:
                # AGI Usage error
                if (data['response'].endswith('Proper usage not available.') or
                        data['response'].endswith('520 End of proper usage.')):
                    pass

                else:
                    return False, None, message.encode()

            elif status in (AGICode.TRYING, AGICode.INVALID_COMMAND, AGICode.COMMAND_NOT_PERMITTED):
                # Without result and data.
                pass

            elif status == AGICode.MEMORY_ALLOCATION_FAILURE:
                agi_server_logger.critical('Unhandled code or undefined response: %s', status)

        else:
            agi_server_logger.warning('Undefined response: %s', message)
            return True, None, None

        return False, AGIMessage(status, result, message_data, info), None


class AGIClientPayloadParser:
    escape_arg_p = re.compile('".+?"')

    def __init__(self, payload):
        self.payload = payload
        self._tail = b''

    def feed_eof(self):
        self.payload.feed_eof()

    def feed_data(self, data, sep=b'\n'):
        if self._tail:
            data, self._tail = self._tail + data, b''

        start_pos = 0
        data_len = len(data)

        lines = []
        while start_pos < data_len:
            pos = data.find(sep, start_pos)
            if pos >= start_pos:
                line = data[start_pos:pos]
                lines.append(line)
                start_pos = pos + 1

            else:
                self._tail = data[start_pos:]
                break

        if not lines:
            return False, self._tail

        eof = False

        for eof, message, payload in self.parse_message(lines):
            if eof:
                self.payload.feed_eof()
                break
            elif message:
                self.payload.feed_data(message, len(payload))

        return eof, self._tail

    def parse_message(self, lines: typing.List[bytes]):
        for line in lines:
            eof = False
            data = line.decode('utf-8')

            if line.lower().startswith(b'failure'):
                yield True, None, ''

            for command in AGICommand.__members__.values():
                if not data.startswith(command.value):
                    continue

                if command == AGICommand.HANGUP:
                    eof = True

                args = self.parse_args(data.split(command.value)[-1])
                yield eof, AGIClientMessage(command, args), line
                break

            else:
                agi_client_logger.warning('Invalid command: {}'.format(data))

    def parse_args(self, line: str):
        line = line.strip()
        split_line = line.split('"')
        args = [args_space.split() for args_space in split_line[::2] if args_space]
        strings = split_line[1::2]
        if not len(split_line) % 2 and strings:
            args.append(strings.pop().strip())

        full_args = []
        list1, list2 = (strings, args) if line.startswith('"') else (args, strings)
        for arg1_arg2 in zip_longest(list1, list2):
            for arg in arg1_arg2:
                if not arg:
                    continue

                if isinstance(arg, list):
                    full_args.extend(arg)
                else:
                    full_args.append(arg)

        return full_args
