from __future__ import print_function

from metakernel import MetaKernel, ProcessMetaKernel, REPLWrapper, u
from metakernel.pexpect import which
import subprocess
import re
import os

from . import __version__


class PsyshKernel(ProcessMetaKernel):
    implementation = 'PsySH Kernel'
    implementation_version = __version__,
    language = 'php'
    language_version = __version__,
    banner = "PsySH Kernel",
    language_info = {
        'mimetype': 'text/x-php',
        'name': 'psysh',
        'language': 'php',
        'file_extension': 'php',
        "version": __version__,
        'help_links': MetaKernel.help_links,
    }

    _setup = """
    more off;
    """

    _banner = None

    _executable = None

    @property
    def executable(self):
        if self._executable:
            return self._executable
        executable = os.environ.get('PSYSH_EXECUTABLE', None)
        if not executable or not which(executable):
            if which('psysh'):
                self._executable = 'psysh'
                return self._executable
            else:
                msg = ('PsySH executable not found, please add to path or set'
                       '"PSYSH_EXECUTABLE" environment variable')
                raise OSError(msg)
        else:
            self._executable = executable
            return executable

    @property
    def banner(self):
        if self._banner is None:
            banner = subprocess.check_output([self.executable, '--version'])
            self._banner = banner.decode('utf-8')
        return self._banner

    def makeWrapper(self):
        """Start an PsySH process and return a :class:`REPLWrapper` object.
        """

        executable = self.executable

        wrapper = REPLWrapper(executable, u('>>>'), None, continuation_prompt_regex=u('\.\.\.'), echo=True)
        wrapper.child.linesep = '\n'
        return wrapper

    def do_execute_direct(self, code):
        # Strip out any php tags.
        super(PsyshKernel, self).do_execute_direct(re.sub(r"<\?php[ \t]*", '', code), self.Print)

    def get_kernel_help_on(self, info, level=0, none_on_fail=False):
        obj = info.get('help_obj', '')
        if not obj or len(obj.split()) > 1:
            if none_on_fail:
                return None
            else:
                return ""
        resp = super(PsyshKernel, self).do_execute_direct('help %s' % obj)
        return str(resp)

    # def get_completions(self, info):
    #     """
    #     Get completions from kernel based on info dict.
    #     """
    #     cmd = '$sh = new \Psy\Shell(); $sh->autocomplete("%s");' % info['obj']
    #     resp = super(PsyshKernel, self).do_execute_direct(cmd)
    #     return str(resp).splitlines()
