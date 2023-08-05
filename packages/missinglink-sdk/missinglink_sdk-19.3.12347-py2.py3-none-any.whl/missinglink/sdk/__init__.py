# -*- coding: utf8 -*-
import logging
import os.path
import sys

from .conda_util import is_conda_env, get_latest_conda_version, conda_install
from .pip_util import get_latest_pip_version, pip_install, get_pip_server
from .sdk_version import get_version, get_keywords

loaded = False
__version__ = get_version()
keywords = get_keywords() or []


logger = logging.getLogger('missinglink')


# noinspection PyBroadException
def update_sdk(latest_version, throw_exception):
    args, p = call_update(latest_version)

    if p is None:
        return False

    try:
        std_output, std_err = p.communicate()
    except Exception:
        if throw_exception:
            raise

        logger.exception("%s failed", " ".join(args))
        return False

    rc = p.returncode

    if rc != 0:
        logger.error('MissingLink SDK failed to upgrade to latest version (%s)', latest_version)
        logger.error("failed to run %s (%s)\n%s\n%s", " ".join(args), rc, std_err, std_output)
        return False

    logger.info('MissingLink SDK updated to latest version (%s)', latest_version)

    return True


def call_update(latest_version):
    require_package = 'missinglink-sdk==%s' % latest_version
    if not is_conda_env():
        running_under_virtualenv = __in_venv()
        should_use_user_path = not running_under_virtualenv
        if should_use_user_path:
            logger.info('updating missing link sdk to version %s in user path', latest_version)
        p, args = pip_install(get_pip_server(keywords), require_package, should_use_user_path)
    else:
        p, args = conda_install(keywords, require_package)
    return args, p


def __in_venv():
    if hasattr(sys, 'real_prefix'):
        # virtualenv venvs
        result = True
    else:
        # PEP 405 venvs
        result = sys.prefix != getattr(sys, 'base_prefix', sys.prefix)

    return result


def self_update(throw_exception=False):
    global __version__

    version = get_version()

    if version is None:
        __version__ = 'Please install this project with setup.py'
        return

    if is_conda_env():
        latest_version = get_latest_conda_version(keywords, throw_exception=throw_exception)
    else:
        latest_version = get_latest_pip_version(keywords, throw_exception=throw_exception)

    if latest_version is None:
        return

    if str(version) == latest_version:
        return

    return update_sdk(latest_version, throw_exception=throw_exception)


global_root_logger_sniffer = None


def do_import():
    import missinglink_kernel

    global global_root_logger_sniffer

    global __version__
    __version__ = missinglink_kernel.get_version()

    from missinglink_kernel import \
        KerasCallback, TensorFlowProject, PyTorchProject, PyCaffeCallback, \
        ExperimentStopped, SkLearnProject, VanillaProject, \
        MissingLinkException, set_global_root_logger_sniffer

    set_global_root_logger_sniffer(global_root_logger_sniffer)

    return KerasCallback, TensorFlowProject, PyTorchProject, PyCaffeCallback, SkLearnProject, ExperimentStopped, MissingLinkException, VanillaProject


def self_update_if_not_disabled():
    if os.environ.get('MISSINGLINKAI_DISABLE_SELF_UPDATE') is None:
        self_update()


# This will store all the logs in memory until the first callback is created and will take control
class GlobalRootLoggerSniffer(logging.Handler):
    MAX_BACKLOGS = 1000

    def __init__(self):
        super(GlobalRootLoggerSniffer, self).__init__(logging.DEBUG)
        self.set_name('ml_global_logs_handler')
        self.root_logger = logging.getLogger()
        self.log_records = []

    def emit(self, record):
        self.log_records.append(record)

        while len(self.log_records) > self.MAX_BACKLOGS:
            self.log_records.pop(0)

    def start_capture_global(self):
        self.root_logger.addHandler(self)  # to catch direct root logging

    def stop_capture_global(self):
        self.root_logger.removeHandler(self)


def set_logger_debug():
    root_logger = logging.getLogger()
    prev_logger_level = root_logger.level
    if root_logger.level != logging.DEBUG:
        root_logger.setLevel(logging.DEBUG)

        for handler in root_logger.handlers:
            handler.setLevel(prev_logger_level)


def catch_logs():
    global global_root_logger_sniffer

    global_root_logger_sniffer = GlobalRootLoggerSniffer()
    global_root_logger_sniffer.start_capture_global()


def setup_global_exception_handler():
    if os.environ.get('MISSINGLINKAI_DISABLE_EXCEPTION_HOOK') is not None:
        return

    import sys
    import traceback
    from missinglink.core.exceptions import MissingLinkException as MissingLinkExceptionCore

    def except_hook(exc_type, value, tb):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, value, tb)
            return

        unhandled_logger = logging.getLogger('unhandled')

        if isinstance(value, MissingLinkExceptionCore):
            unhandled_logger.critical('[%s] %s', exc_type.__name__, value)
        else:
            message = ''.join(traceback.format_exception(exc_type, value, tb))
            unhandled_logger.critical(message)

        sys.__excepthook__(exc_type, value, tb)

    sys.excepthook = except_hook


set_logger_debug()
catch_logs()
self_update_if_not_disabled()
setup_global_exception_handler()

KerasCallback, TensorFlowProject, PyTorchProject, PyCaffeCallback, SkLearnProject, ExperimentStopped, MissingLinkException, VanillaProject = do_import()


def debug_missinglink_on():
    logging.basicConfig()
    missinglink_log = logging.getLogger('missinglink')
    missinglink_log.setLevel(logging.DEBUG)
    missinglink_log.propagate = False
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s.%(msecs)03d %(name)s %(levelname)s %(message)s', '%Y-%m-%d %H:%M:%S')
    ch.setFormatter(formatter)
    missinglink_log.addHandler(ch)
