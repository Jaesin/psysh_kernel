from __future__ import print_function

import json
import os
import sys
import uuid

from metakernel import MetaKernel, ProcessMetaKernel, REPLWrapper, u
from metakernel.pexpect import which

from . import __version__


STDIN_PROMPT = '>>> '

def get_kernel_json():
    """Get the kernel json for the kernel.
    """
    # Load the kernel data from the kernel.json file directly.
    with open(os.path.join(os.path.dirname(__file__), 'kernel.json')) as json_raw:
        kernel_json = json.load(json_raw)
    # Set the current executable as the kernel executable.
    kernel_json['argv'][0] = sys.executable
    return kernel_json

class PsyshKernel(ProcessMetaKernel):
    implementation = 'PsySH Kernel'
    implementation_version = __version__,
    language = 'php'
    help_links = [
        {
            'text': "The PHP Manual",
            'url': "http://php.net/docs.php",
        },
        {
            'text': "PsySH",
            'url': "https://psysh.org/",
        },
        {
            'text': "PsySH Kernel",
            'url': "https://github.com/Jaesin/psysh_kernel/",
        },
    ] + MetaKernel.help_links
    kernel_json = get_kernel_json()

    _php_engine = None
    _language_version = None
    _shell_version = None
    _shell_location = None

    @property
    def language_version(self):
        if self._language_version is None:
            self._language_version = self.php_engine.eval('PHP_VERSION', silent=True)[9:-7]

        return self._language_version

    @property
    def shell_version(self):
        if self._shell_version is None:
            self._shell_version = self.php_engine.eval('\Psy\Shell::VERSION', silent=True)[9:-7]

        return self._shell_version

    @property
    def shell_location(self):
        if self._shell_location is None:
            self._shell_location = self.php_engine.eval('get_included_files()[0];', silent=True)[9:-8]

        return self._shell_location

    @property
    def language_info(self):
        return {'mimetype': 'text/x-php',
                'name': 'php',
                'file_extension': '.php',
                'version': self.language_version,
                'help_links': self.help_links}

    @property
    def banner(self):
        msg = '''PsySH Kernel version: %s
Kernel location: %r

PsySH version: %s (%r)
PHP version: %s.
'''
        return msg % (__version__, __file__, self.shell_version, self.shell_location, self.language_version)

    @property
    def php_engine(self):
        if self._php_engine is None:
            self._php_engine = PhpEngine(
                error_handler=self.Error,
                stdin_handler=self.raw_input,
                stream_handler=self.Print,
                logger=self.log)
        return self._php_engine

    def makeWrapper(self):
        """Start an Psysh process and return a :class:`REPLWrapper` object.
        """
        return self.php_engine.repl

    def do_execute_direct(self, code, silent=False):
        if code.strip() in ['quit', 'quit()', 'exit', 'exit()']:
            self._php_engine = None
            self.do_shutdown(True)
            return
        val = ProcessMetaKernel.do_execute_direct(self, code, silent=silent)
        return val

    def get_kernel_help_on(self, info, level=0, none_on_fail=False):
        obj = info.get('help_obj', '')
        if not obj or len(obj.split()) > 1:
            if none_on_fail:
                return None
            else:
                return ""
        return self.php_engine.eval('help %s' % obj, silent=True)

    def Print(self, *args, **kwargs):
        # Ignore standalone input hook displays.
        out = []
        for arg in args:
            if arg.strip() == STDIN_PROMPT:
                return
            if arg.strip().startswith(STDIN_PROMPT):
                arg = arg.replace(STDIN_PROMPT, '')
            out.append(arg)
        super(PsyshKernel, self).Print(*out, **kwargs)

    def raw_input(self, prompt=''):
        # Remove the stdin prompt to restore the original prompt.
        prompt = prompt.replace(STDIN_PROMPT, '')
        return super(PsyshKernel, self).raw_input(prompt)

    def get_completions(self, info):
        """
        Get completions from kernel based on info dict.
        """
        val = self.php_engine.eval('%s\t' % info['obj'], silent=True)
        return val and val.splitlines() or []


class PhpEngine(object):

    def __init__(self, error_handler=None, stream_handler=None,
                 stdin_handler=None,
                 logger=None):
        self.logger = logger
        self.executable = self._get_executable()
        self.repl = self._create_repl()
        self.error_handler = error_handler
        self.stream_handler = stream_handler
        self.stdin_handler = stdin_handler

    def eval(self, code, timeout=None, silent=False):
        """Evaluate code using the engine.
        """
        stream_handler = None if silent else self.stream_handler
        if self.logger:
            self.logger.debug('PHP eval:')
            self.logger.debug(code)
        try:
            resp = self.repl.run_command(code.rstrip(),
                                         timeout=timeout,
                                         stream_handler=stream_handler,
                                         stdin_handler=self.stdin_handler)
            resp = resp.replace(STDIN_PROMPT, '')
            if self.logger and resp:
                self.logger.debug(resp)
            return resp
        except KeyboardInterrupt:
            return self._interrupt(True)
        except Exception as e:
            if self.error_handler:
                self.error_handler(e)
            else:
                raise e

    def _startup(self):
        self.eval('cd("%s");%s' % (os.getcwd().replace(os.path.sep, '/'), self.repl.prompt_change_cmd), silent=True)

    def _create_repl(self):
        repl = REPLWrapper(self.executable, STDIN_PROMPT, None,
                           stdin_prompt_regex=r'\A>>> ',
                           continuation_prompt_regex=r'\A\.\.\. ',
                           echo=True)
        if os.name == 'nt':
            repl.child.crlf = '\n'
        repl.interrupt = self._interrupt
        # Remove the default 50ms delay before sending lines.
        repl.child.delaybeforesend = None
        return repl

    def _interrupt(self, silent=False):
        return REPLWrapper.interrupt(self.repl)

    def _interrupt_expect(self, silent):
        repl = self.repl
        child = repl.child
        expects = [repl.prompt_regex, child.linesep]
        expected = uuid.uuid4().hex
        repl.sendline('disp("%s");' % expected)
        if repl.prompt_emit_cmd:
            repl.sendline(repl.prompt_emit_cmd)
        lines = []
        while True:
            # Prevent a keyboard interrupt from breaking this up.
            while True:
                try:
                    pos = child.expect(expects)
                    break
                except KeyboardInterrupt:
                    pass
            if pos == 1:  # End of line received
                line = child.before
                if silent:
                    lines.append(line)
                else:
                    self.stream_handler(line)
            else:
                line = child.before
                if line.strip() == expected:
                    break
                if len(line) != 0:
                    # prompt received, but partial line precedes it
                    if silent:
                        lines.append(line)
                    else:
                        self.stream_handler(line)
        return '\n'.join(lines)

    def _get_executable(self):
        """Find the psysh executable.
        """
        executable = os.environ.get('PSYSH_EXECUTABLE', None)
        if not executable or not which(executable):
            if which('psysh'):
                executable = 'psysh'
            else:
                msg = ('PsySH Executable not found, please add to path or set'
                       '"PSYSH_EXECUTABLE" environment variable')
                raise OSError(msg)
        executable = executable.replace(os.path.sep, '/')
        return executable
