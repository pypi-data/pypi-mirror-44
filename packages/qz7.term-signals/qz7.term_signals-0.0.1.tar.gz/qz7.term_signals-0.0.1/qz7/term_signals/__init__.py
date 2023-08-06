"""
Functions for gracefully handling TERM signals.
"""

import signal
import logging
from functools import partial

TERM_SIGNALS = ["SIGINT", "SIGQUIT", "SIGHUP", "SIGTERM"]

TERM_SIGNAL_RECEIVED = []

log = logging.getLogger(__name__)

class TermSignalException(KeyboardInterrupt):
    def __init__(self, signame, signum, frame):
        super().__init__("Received %s(%d)" % (signame, signum))

        self.signame = signame
        self.signum = signum
        self.frame = frame

def handle_term_signal(signame, raise_exc, signum, frame):
    """
    Handle the given term signal.
    """

    log.info("Received %s(%d)", signame, signum)

    TERM_SIGNAL_RECEIVED.append(signame)

    if raise_exc:
        raise TermSignalException(signame, signum, frame)

def have_received_term_signal():
    """
    Return the list of term signals received.
    """

    return TERM_SIGNAL_RECEIVED

def register_term_signal_handlers(raise_exc):
    """
    Register term signal handlers.
    """

    for signame in TERM_SIGNALS:
        signal.signal(getattr(signal, signame), partial(handle_term_signal, signame, raise_exc))
