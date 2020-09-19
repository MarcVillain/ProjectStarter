import logging

_logger = logging.getLogger("ProjectStarter")


def setup(verbose):
    # Set logging level
    log_level = logging.DEBUG if verbose else logging.INFO
    _logger.setLevel(log_level)

    # Enable logging in stdout
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)
    _logger.addHandler(stream_handler)


def _log(func, msg, prefix, *args, **kwargs):
    func(f"{prefix or ''}{msg}", *args, **kwargs)


def info(msg, prefix=None, *args, **kwargs):
    _log(_logger.info, msg, prefix, *args, **kwargs)


def error(msg, prefix=None, *args, **kwargs):
    _log(_logger.error, f"error: {msg}", prefix, *args, **kwargs)


def warning(msg, prefix=None, *args, **kwargs):
    _log(_logger.warning, f"warning: {msg}", prefix, *args, **kwargs)


def debug(msg, prefix=None, *args, **kwargs):
    _log(_logger.debug, f"debug: {msg}", prefix, *args, **kwargs)
