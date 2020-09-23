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


def _log(func, msg, prefix, **kwargs):
    func(f"{prefix or ''}{msg}", **kwargs)


def info(msg, *args, prefix=None, **kwargs):
    if len(args) > 0:
        msg = f"{msg} {' '.join(args)}"
    _log(_logger.info, msg, prefix, **kwargs)


def error(msg, *args, prefix=None, **kwargs):
    if len(args) > 0:
        msg = f"{msg} {' '.join(args)}"
    _log(_logger.error, f"error: {msg}", prefix, **kwargs)


def warning(msg, *args, prefix=None, **kwargs):
    if len(args) > 0:
        msg = f"{msg} {' '.join(args)}"
    _log(_logger.warning, f"warning: {msg}", prefix, **kwargs)


def debug(msg, *args, prefix=None, **kwargs):
    if len(args) > 0:
        msg = f"{msg} {' '.join(args)}"
    _log(_logger.debug, f"debug: {msg}", prefix, **kwargs)
