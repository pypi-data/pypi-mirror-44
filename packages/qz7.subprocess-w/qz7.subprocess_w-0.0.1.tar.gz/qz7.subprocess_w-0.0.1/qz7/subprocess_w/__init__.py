"""
Subprocess wrapper

Proivdes a subclass of Popen,
that terminates gracefully instead of leaving zombie/orphan subprocesses.
"""

import logging
from subprocess import (
    Popen, PIPE, STDOUT,
    TimeoutExpired,
    CalledProcessError,
    CompletedProcess
)

log = logging.getLogger(__name__)

DEFAULT_WAIT_TIMEOUT = 0
DEFAULT_TERM_TIMEOUT = 30

class PopenW(Popen):
    """
    Popen wrapper that exits gracefully.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        log.info("Starting %d: %s", self.pid, self.args)
        self._log_dead = True

    def is_dead(self):
        """
        Check and log if the process is dead.
        """

        if self.poll() is not None:
            if self._log_dead:
                log.info("Exited %d: %s", self.pid, self.args)
                self._log_dead = False

            return True

        return False

    def terminate_gracefully(self,
                             wait_timeout=DEFAULT_WAIT_TIMEOUT,
                             term_timeout=DEFAULT_TERM_TIMEOUT):
        """
        Terminate the process gracefully.
        """

        if self.poll() is not None:
            if self._log_dead:
                log.info("Exited %d: %s", self.pid, self.args)
                self._log_dead = False
            return

        try:
            self.wait(timeout=wait_timeout)
        except TimeoutExpired:
            log.info("Terminating %d: %s", self.pid, self.args)
            self.terminate()
            try:
                self.wait(timeout=term_timeout)
            except TimeoutExpired:
                log.warning("Killing %d: %s", self.pid, self.args)
                self.kill()
                self.wait()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, value, traceback):
        self.terminate_gracefully()

    def __del__(self):
        self.terminate_gracefully()
