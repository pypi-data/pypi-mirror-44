"""
This module contains functions and classes to implment AGI scripts in python.
"""
import asyncio

from aiohttp import EofStream

from aioagi.commands import AGICommand
from aioagi.exceptions import (
    AGIResultHangup, AGIConnectHangup,
    AGIUsageError, AGIInvalidCommand,
    AGIAppError, AGICommandNotPermittedError
)
from aioagi.parser import AGIMessage, AGICode
from aioagi.request import AGIRequest

DEFAULT_TIMEOUT = 2000  # 2sec timeout used as default for functions that take timeouts
DEFAULT_RECORD = 20000  # 20sec record time


class AGI:
    """
    This class encapsulates communication between Asterisk an a python script.
    It handles encoding commands to Asterisk and parsing responses from
    Asterisk.
    """

    def __init__(self, request: AGIRequest):
        """
        request.headers = {
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
        self.request = request
        self.headers = request.headers
        self.lock = asyncio.Lock()

    def _quote(self, string):
        return '"{}"'.format(str(string))

    def _process_digit_list(self, digits):
        if isinstance(digits, (list, tuple)):
            digits = ''.join(map(str, digits))
        return self._quote(digits)

    async def run_command(self, command: AGICommand, *args) -> AGIMessage:
        """
        Run a command to Asterisk

        If any command returned `-1` - raise AGIAppError.
        This means that chanel return error or hangup.
        """
        command = command.value
        command = '{} {}'.format(command, ' '.join(map(str, args)))
        command = command.strip()
        if command[-1] != '\n':
            command += '\n'

        async with self.lock:
            try:
                await self.request.writer.write(command)
                await self.request.writer.drain()
                message = await self.request.reader.read()
                if message.status == AGICode.TRYING:
                    message = await self.request.reader.read()

            except EofStream:
                raise AGIResultHangup()
            except (asyncio.CancelledError, ConnectionResetError):
                raise AGIConnectHangup()

        if message.status == AGICode.MEMORY_ALLOCATION_FAILURE:
            raise AGIInvalidCommand(error=message.info)
        elif message.status == AGICode.INVALID_COMMAND:
            raise AGIInvalidCommand(error=message.info)
        elif message.status == AGICode.COMMAND_NOT_PERMITTED:
            raise AGICommandNotPermittedError(error=message.info)
        elif message.status == AGICode.INVALID_COMMAND_SYNTAX:
            raise AGIUsageError(error=message.info)
        elif message.result == '-1':
            raise AGIAppError(message='Error executing application, or hangup.'.encode())

        return message

    async def answer(self):
        """
        Answer channel

        Answers channel if not already in answer state.
        Returns -1 on channel failure, or 0 if successful.
        """
        return await self.run_command(AGICommand.ANSWER)

    async def channel_status(self, channel=''):
        """
        Returns status of the connected channel.

        Returns the status of the specified channelname.
        If no channel name is given then returns the status of the current channel.

        Return values:
        0 - Channel is down and available.
        1 - Channel is down, but reserved.
        2 - Channel is off hook.
        3 - Digits (or equivalent) have been dialed.
        4 - Line is ringing.
        5 - Remote end is ringing.
        6 - Line is up.
        7 - Line is busy.
        """
        message = await self.run_command(AGICommand.CHANNEL_STATUS, channel)
        return message.result_to_int()

    async def control_stream_file(self, filename, escape_digits='', skipms=3000, fwd='', rew='', pause=''):
        """
        Sends audio file on channel and allows the listener to control the stream.

        Use double quotes for the digits if you wish none to be permitted.
        Returns 0 if playback completes without a digit being pressed,
        or the ASCII numerical value of the digit if one was pressed,
        or -1 on error or if the channel was disconnected.

        Send the given file, allowing playback to be interrupted by the given
        digits, if any.  escape_digits is a string '12345' or a list  of
        ints [1,2,3,4,5] or strings ['1','2','3'] or mixed [1,'2',3,'4']
        If sample offset is provided then the audio will seek to sample
        offset before play starts.  Returns  digit if one was pressed.
        Throws AGIAppError if the channel was disconnected.  Remember, the file
        extension must not be included in the filename.
        """
        message = await self.run_command(
            AGICommand.CONTROL_STREAM_FILE,
            self._quote(filename),
            self._process_digit_list(escape_digits),
            self._quote(skipms),
            self._quote(fwd),
            self._quote(rew),
            self._quote(pause)
        )
        return message.result_to_char()

    async def database_del(self, family, key):
        """
        Removes database key/value.

        Deletes an entry in the Asterisk database for a
        given family and key.
        Returns 1 if successful, 0 otherwise.
        """
        message = await self.run_command(
            AGICommand.DATABASE_DEL,
            self._quote(family),
            self._quote(key)
        )
        return message.result_to_bool()

    async def database_deltree(self, family, key=''):
        """
        Removes database keytree/value.

        Deletes a family or specific keytree with in a family in the Asterisk database.
        Returns 1 if successful, 0 otherwise.
        """
        message = await self.run_command(
            AGICommand.DATABASE_DELTREE,
            self._quote(family),
            self._quote(key)
        )
        return message.result_to_bool()

    async def database_get(self, family, key):
        """
        Gets database value.

        Retrieves an entry in the Asterisk database for a given family and key.
        Returns 0 if <key> is not set.  Returns 1 if <key>
        is set and returns the variable in parenthesis.
        Example return code: `200 result=1 (testvariable)`.
        """
        message = await self.run_command(
            AGICommand.DATABASE_GET,
            self._quote(family),
            self._quote(key)
        )
        return message.result_to_bool()

    async def database_put(self, family, key, value):
        """
        Adds/updates database value

        Adds or updates an entry in the Asterisk database for a
        given family, key, and value.
        Returns 1 if successful, 0 otherwise.
        """
        message = await self.run_command(
            AGICommand.DATABASE_PUT,
            self._quote(family),
            self._quote(key),
            self._quote(value)
        )
        return message.result_to_bool()

    async def exec_app(self, application, options=''):
        """
        Executes a given Application.

        Executes <application> with given <options>.
        Returns whatever the application returns, or -2 on failure to find
        application
        """
        message = await self.run_command(AGICommand.EXEC, application, self._quote(options))
        if message.result == '-2':
            raise AGIAppError(message='Unable to find application: %s' % application)
        return message

    async def get_data(self, filename, timeout=DEFAULT_TIMEOUT, max_digits=255):
        """
        Prompts for DTMF on a channel.

        Stream the given file, and receive DTMF data.
        Returns the digits received from the channel at the other end.
        Example: `200 result=132456`.
        """
        return await self.run_command(AGICommand.GET_DATA, filename, timeout, max_digits)

    async def get_full_variable(self, name, channel=None):
        """
        Evaluates a channel expression.

        Returns 0 if variablename is not set or channel does not exist.
        Returns 1 if variablename is set and returns the variable in parenthesis.
        Understands complex variable names and builtin variables, unlike GET VARIABLE.

        Example return code: `200 result=1 (testvariable)`
        """
        args = [AGICommand.GET_FULL_VARIABLE, self._quote(name)]
        if channel:
            args.append(self._quote(channel))

        message = await self.run_command(*args)
        return message.result_to_bool()

    async def get_option(self, filename, escape_digits='', timeout=0):
        """
        Stream file, prompt for DTMF, with timeout.

        Behaves similar to STREAM FILE but used with a timeout option.

        Send the given file, allowing playback to be interrupted by the given
        digits, if any.  escape_digits is a string '12345' or a list  of
        ints [1,2,3,4,5] or strings ['1','2','3'] or mixed [1,'2',3,'4']
        Returns  digit if one was pressed.
        Remember, the file extension must not be included in the filename.
        """
        escape_digits = self._process_digit_list(escape_digits)
        args = [AGICommand.GET_OPTION, filename, escape_digits]
        if timeout:
            args.append(timeout)

        message = await self.run_command(*args)
        return message.result_to_char()

    async def get_variable(self, name):
        """
        Get a channel variable.

        Returns 0 if variablename is not set.
        Returns 1 if variablename is set and returns the variable in parentheses.
        Example return code: `200 result=1 (testvariable)`.

        This function returns the value of the indicated channel variable.
        """
        message = await self.run_command(
            AGICommand.GET_VARIABLE,
            self._quote(name)
        )

        return message.result_to_bool()

    async def gosub(self, context, extension, priority, *args):
        """
        Cause the channel to execute the specified dialplan subroutine.

        Cause the channel to execute the specified dialplan subroutine,
        returning to the dialplan with execution of a Return().
        """
        message = await self.run_command(
            AGICommand.GOSUB,
            context, extension, priority,
            '{}'.format(','.join(map(str, args)))
        )
        return message

    async def goto_on_exit(self, context='', extension='', priority=''):
        """
        Set endpoint in dialplan on exit.
        Group execute `set_context`, `set_extension` and `set_priority`.
        """
        await self.set_context(context or self.headers['agi_context'])
        await self.set_extension(extension or self.headers['agi_extension'])
        await self.set_priority(priority or self.headers['agi_priority'])

    async def hangup(self, channel=''):
        """
        Hangup a channel.

        Hangs up the specified channel.
        If no channel name is given, hangs up the current channel.
        """
        return await self.run_command(AGICommand.HANGUP, channel)

    async def noop(self):
        """
        Does nothing.
        """
        return await self.run_command(AGICommand.NOOP)

    async def receive_char(self, timeout=DEFAULT_TIMEOUT):
        """
        Receives one character from channels supporting it.

        Returns the decimal value of the character if one is received,
        or 0 if the channel does not support text reception.
        Returns -1 only on error/hangup.

        Receives a character of text on a channel. Specify timeout to be the
        maximum time to wait for input in milliseconds, or 0 for infinite.
        Most channels do not support the reception of text.
        """
        message = await self.run_command(AGICommand.RECEIVE_CHAR, timeout)
        return message.result_to_char()

    async def receive_text(self, timeout=DEFAULT_TIMEOUT):
        """
        Receives text from channels supporting it.

        Receives a string of text on a channel.
        Most channels do not support the reception of text.
        Returns -1 for failure or 1 for success, and the string in parenthesis.
        """
        message = await self.run_command(AGICommand.RECEIVE_TEXT, timeout)
        return message

    async def record_file(self,
                          filename, audio_format='gsm',
                          escape_digits='#', timeout=DEFAULT_RECORD, offset=0,
                          beep='beep', silence: int = None):
        """
        Records to a given file.

        Record to a file until a given dtmf digit in the sequence is received
        The format will specify what kind of file will be recorded.  The timeout
        is the maximum record time in milliseconds, or -1 for no timeout. Offset
        samples is optional, and if provided will seek to the offset without
        exceeding the end of the file

        :param filename: The destination filename of the recorded audio.
        :param audio_format: The audio format in which to save the resulting file.
        :param escape_digits: The DTMF digits that will terminate the recording process.
        :param timeout: The maximum recording time in milliseconds. Set to -1 for no limit.
        :param offset: Causes the recording to first seek to the specified offset before recording begins.
        :param beep: Causes Asterisk to play a beep as recording begins. This argument can take any value.
        :param silence: The number of seconds of silence that are permitted before the recording is terminated,
                        regardless of the escape_digits or timeout arguments.
                        If specified, this parameter must be preceded by s=.
        """
        escape_digits = self._process_digit_list(escape_digits)
        args = [
            AGICommand.RECORD_FILE, self._quote(filename), audio_format,
            escape_digits, timeout, offset, beep,
        ]
        if silence:
            args.append('s={}'.format(silence))

        return await self.run_command(*args)

    async def say_alpha(self, characters, escape_digits=''):
        """
        Says a given character string.

        Say a given character string, returning early if any of the given DTMF
        digits are received on the channel.
        Throws AGIAppError on channel failure
        """
        characters = self._process_digit_list(characters)
        escape_digits = self._process_digit_list(escape_digits)
        message = await self.run_command(AGICommand.SAY_ALPHA, characters, escape_digits)
        return message.result_to_char()

    async def say_date(self, seconds, escape_digits=''):
        """
        Says a given date.

        Say a given date, returning early if any of the given DTMF digits are
        received on the channel.
        Returns 0 if playback completes without a digit being pressed,
        or the ASCII numerical value of the digit if one was pressed or -1 on error/hangup.

        The date should be in seconds since the UNIX Epoch (Jan 1, 1970 00:00:00)

        :param seconds: Is number of seconds elapsed since 00:00:00 on January 1, 1970.
                        Coordinated Universal Time (UTC).
        """
        escape_digits = self._process_digit_list(escape_digits)
        message = await self.run_command(AGICommand.SAY_DATE, seconds, escape_digits)
        return message.result_to_char()

    async def say_datetime(self, seconds, escape_digits='', format='', zone=''):
        """
        Says a given time as specified by the format given.

        Say a given time, returning early if any of the given DTMF digits are received on the channel.
        Returns 0 if playback completes without a digit being pressed,
        or the ASCII numerical value of the digit if one was pressed or -1 on error/hangup.

        :param seconds: Is number of seconds elapsed since 00:00:00 on January 1, 1970, Coordinated Universal Time (UTC)
        :param escape_digits: экранированные цифры
        :param format: Is the format the time should be said in. See voicemail.conf (defaults to ABdY 'digits/at' IMp).
        :param zone: Acceptable values can be found in /usr/share/zoneinfo Defaults to machine default.
        """
        escape_digits = self._process_digit_list(escape_digits)
        if format:
            format = self._quote(format)

        message = await self.run_command(
            AGICommand.SAY_DATETIME,
            seconds,
            escape_digits,
            format,
            zone
        )
        return message.result_to_char()

    async def say_digits(self, digits, escape_digits=''):
        """
        Says a given digit string.

        Say a given digit string, returning early if any of the given DTMF digits are received on the channel.
        Returns 0 if playback completes without a digit being pressed,
        or the ASCII numerical value of the digit if one was pressed or -1 on error/hangup.
        """
        digits = self._process_digit_list(digits)
        escape_digits = self._process_digit_list(escape_digits)
        message = await self.run_command(AGICommand.SAY_DIGITS, digits, escape_digits)
        return message.result_to_char()

    async def say_number(self, number, escape_digits=''):
        """
        Says a given number.

        Say a given number, returning early if any of the given DTMF digits are received on the channel.
        Returns 0 if playback completes without a digit being pressed,
        or the ASCII numerical value of the digit if one was pressed or -1 on error/hangup.
        """
        number = self._process_digit_list(number)
        escape_digits = self._process_digit_list(escape_digits)
        message = await self.run_command(AGICommand.SAY_NUMBER, number, escape_digits)
        return message.result_as_char()

    async def say_phonetic(self, characters, escape_digits=''):
        """
        Says a given character string with phonetics.

        Say a given character string with phonetics,
        returning early if any of the given DTMF digits are received on the channel.
        Returns 0 if playback completes without a digit pressed,
        the ASCII numerical value of the digit if one was pressed, or -1 on error/hangup.
        """
        characters = self._process_digit_list(characters)
        escape_digits = self._process_digit_list(escape_digits)
        message = await self.run_command(
            AGICommand.SAY_PHONETIC, characters, escape_digits
        )
        return message.result_to_char()

    async def say_time(self, seconds, escape_digits=''):
        """
        Says a given time.

        Say a given time, returning early if any of the given DTMF digits are received on the channel.
        Returns 0 if playback completes without a digit being pressed,
        or the ASCII numerical value of the digit if one was pressed or -1 on error/hangup.

        :param time: Is number of seconds elapsed since 00:00:00 on January 1, 1970. Coordinated Universal Time (UTC).
        :param escape_digits: экранированные числа
        """
        escape_digits = self._process_digit_list(escape_digits)
        message = await self.run_command(AGICommand.SAY_TIME, seconds, escape_digits)
        return message.result_to_char()

    async def send_image(self, filename):
        """
        Sends images to channels supporting it.

        Sends the given image on a channel.
        Most channels do not support the transmission of images.
        Returns 0 if image is sent, or if the channel does not support image transmission.
        Returns -1 only on error/hangup. Image names should not include extensions.
        """
        return await self.run_command(AGICommand.SEND_IMAGE, filename)

    async def send_text(self, text=''):
        """
        Sends text to channels supporting it.

        Sends the given text on a channel.
        Most channels do not support the transmission of text.
        Returns 0 if text is sent, or if the channel does not support text transmission.
        Returns -1 only on error/hangup.
        """
        return await self.run_command(AGICommand.SEND_TEXT, self._quote(text))

    async def set_autohangup(self, secs):
        """
        Autohangup channel in some time.

        Cause the channel to automatically hangup at <secs> seconds in the
        future.  Of course it can be hungup before then as well. Setting to
        0 will cause the autohangup feature to be disabled on this channel.
        """
        await self.run_command(AGICommand.SET_AUTOHANGUP, secs)

    async def set_callerid(self, number):
        """
        Sets callerid for the current channel.

        Changes the callerid of the current channel.
        """
        await self.run_command(AGICommand.SET_CALLERID, number)

    async def set_context(self, context):
        """
        Sets channel context.

        Sets the context for continuation upon exiting the application.
        No error appears to be produced.  Does not set exten or priority
        Use at your own risk.  Ensure that you specify a valid context.
        """
        await self.run_command(AGICommand.SET_CONTEXT, context)

    async def set_music(self, toggle, music='default'):
        """
        Enable/Disable Music on hold generator
        Enables/Disables the music on hold generator.
        If class is not specified, then the default music on hold class will be used.
        This generator will be stopped automatically when playing a file.
        Always returns 0.

        Usage: SET MUSIC <on|off> <class>

        :param music: music class
        :param toggle: on|off
        """
        return await self.run_command(AGICommand.SET_MUSIC, toggle, music)

    async def set_extension(self, extension):
        """
        Changes channel extension.

        Sets the extension for continuation upon exiting the application.
        No error appears to be produced.  Does not set context or priority
        Use at your own risk.  Ensure that you specify a valid extension.
        """
        await self.run_command(AGICommand.SET_EXTENSION, extension)

    async def set_priority(self, priority):
        """
        Set channel dialplan priority.

        Sets the priority for continuation upon exiting the application.
        No error appears to be produced.  Does not set exten or context
        Use at your own risk.  Ensure that you specify a valid priority.
        """
        await self.run_command(AGICommand.SET_PRIORITY, priority)

    async def set_variable(self, name, value):
        """
        Set a channel variable.
        Sets a variable to the current channel.
        """
        await self.run_command(AGICommand.SET_VARIABLE, self._quote(name), self._quote(value))

    async def stream_file(self, filename, escape_digits='', sample_offset=0):
        """
        Sends audio file on channel.

        Send the given file, allowing playback to be interrupted by the given digits, if any.
        Returns 0 if playback completes without a digit being pressed,
        or the ASCII numerical value of the digit if one was pressed,
        or -1 on error or if the channel was disconnected.

        If musiconhold is playing before calling stream file
        it will be automatically stopped and will not be restarted after completion.

        Send the given file, allowing playback to be interrupted by the given
        digits, if any.  escape_digits is a string '12345' or a list  of
        ints [1,2,3,4,5] or strings ['1','2','3'] or mixed [1,'2',3,'4']
        If sample offset is provided then the audio will seek to sample
        offset before play starts.  Returns  digit if one was pressed
        or -1 if error/hangup channel.
        Remember, the file extension must not be included in the filename.
        """
        escape_digits = self._process_digit_list(escape_digits)
        message = await self.run_command(
            AGICommand.STREAM_FILE,
            filename,
            escape_digits,
            sample_offset
        )
        return message.result_to_char()

    async def tdd_mode(self, mode='off'):
        """
        Toggles TDD mode (for the deaf).

        Enable/Disable TDD transmission/reception on a channel.
        Returns 1 if successful, or 0 if channel is not TDD-capable.
        """
        message = await self.run_command(AGICommand.TDD_MODE, mode)
        if message.result == '0':
            raise AGIAppError(message='Channel %s is not TDD-capable')

    async def verbose(self, message, level=1):
        """
        Logs a message to the asterisk verbose log.

        Sends <message> to the console via verbose message system.
        <level> is the the verbose level (1-4).
        Always returns 1.
        """
        await self.run_command(AGICommand.VERBOSE, self._quote(message), level)

    async def wait_for_digit(self, timeout=DEFAULT_TIMEOUT):
        """
        Waits for a digit to be pressed.

        Waits for up to 'timeout' milliseconds for a channel to receive a DTMF digit.
        Waits up to timeout milliseconds for channel to receive a DTMF digit.
        Returns -1 on channel failure, 0 if no digit is received in the timeout,
        or the numerical value of the ascii of the digit if one is received.
        Use -1 for the timeout value if you desire the call to block indefinitely.
        """
        message = await self.run_command(AGICommand.WAIT_FOR_DIGIT, timeout)
        return message.result_to_char()
