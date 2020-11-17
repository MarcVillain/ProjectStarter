import logging

# Create main logger
_logger = logging.getLogger("ProjectStarter")


def setup(verbose=False):
    """
    Setup logging level and output style. The default level of logging is set
    to INFO.
    :param verbose: If True, set logging to DEBUG.
    """
    # Set logging level
    log_level = logging.DEBUG if verbose else logging.INFO
    _logger.setLevel(log_level)

    # Enable logging in stdout
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)
    _logger.addHandler(stream_handler)


def _log(func, msg, prefix, **kwargs):
    """
    Log a message with a '{prefix}{msg}' format.
    :param func: Function to use for logging
    :param msg: Message to log
    :param prefix: Prefix of message
    :param kwargs: Any arguments that can be given to func
    """
    func(f"{prefix or ''}{msg}", **kwargs)


def info(msg, *args, prefix=None, **kwargs):
    """
    Log an info message.
    :param msg: Message to log
    :param prefix: If set, prefix of message
    :param kwargs: Any arguments that can be given to the info function
    """
    if len(args) > 0:
        msg = f"{msg} {' '.join(args)}"
    _log(_logger.info, msg, prefix, **kwargs)


def error(msg, *args, prefix=None, **kwargs):
    """
    Log an error message.
    :param msg: Message to log
    :param prefix: If set, prefix of message
    :param kwargs: Any arguments that can be given to the info function
    """
    if len(args) > 0:
        msg = f"{msg} {' '.join(args)}"
    _log(_logger.error, f"error: {msg}", prefix, **kwargs)


def warning(msg, *args, prefix=None, **kwargs):
    """
    Log a warning message.
    :param msg: Message to log
    :param prefix: If set, prefix of message
    :param kwargs: Any arguments that can be given to the info function
    """
    if len(args) > 0:
        msg = f"{msg} {' '.join(args)}"
    _log(_logger.warning, f"warning: {msg}", prefix, **kwargs)


def debug(msg, *args, prefix=None, **kwargs):
    """
    Log a debug message.
    :param msg: Message to log
    :param prefix: If set, prefix of message
    :param kwargs: Any arguments that can be given to the info function
    """
    if len(args) > 0:
        msg = f"{msg} {' '.join(args)}"
    _log(_logger.debug, f"debug: {msg}", prefix, **kwargs)
