import sys
import logging
import logging.handlers

# set of scripts to simplify usage of logger


def get_log_level(level):
    """
    Convert the provided string to the corresponding logging level.

    :param level: string
    :return: logging level
    """
    if level.upper() == "CRITICAL":
        level = logging.CRITICAL
    elif level.upper() == "ERROR":
        level = logging.ERROR
    elif level.upper() == "WARNING":
        level = logging.WARNING
    elif level.upper() == "INFO":
        level = logging.INFO
    elif level.upper() == "DEBUG":
        level = logging.DEBUG
    elif level.upper() == "NOTSET":
        level = logging.NOTSET
    else:
        raise ValueError("unknown value for logger level ('{}').".format(level))
    return level


def get_child(logger, logger_name, config=None):
    """
    Create a child logger and optionally apply a different log level

    :param logger: logger instance
    :param logger_name: name for the child logger
    :param config: config yaml structure with at least an "log-level" entry.
    :return:
    """
    child = logger.getChild(logger_name)
    if config is not None:
        try:
            log_level = config["log-level"]
            level = get_log_level(log_level)
            child.setLevel(level)
        except KeyError:
            pass
    return child


def create_logger(config, logger_name):
    """
    Create an logger instance with the provided log level and target file.

    :param config: config yaml structure with at least "log-level" and "log-file" as entries
    :param logger_name: name for the logger to be created
    :return: logger instance
    """
    log_level = config["log-level"]
    level = get_log_level(log_level)

    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    if not len(logger.handlers):
        try:
            max_bytes = int(config["log-rotation"]["maxbytes"])
            backup_count = int(config["log-rotation"]["backupcount"])
            handler = logging.handlers.RotatingFileHandler(config["log-file"], maxBytes=max_bytes, backupCount=backup_count)
        except KeyError:
            handler = logging.FileHandler(config["log-file"])
        handler.setLevel(level)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        logger.addHandler(handler)

    return logger


def add_log2stdout_handler(logger, level):
    """
    add a handler to the logger that outputs to the console.

    :param logger: logger instance
    :param level: level in string
    :return:
    """

    if level is not None and level != "":
        log_level = get_log_level(level)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(log_level)
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)


class MyMQTTFilter(logging.Filter):
    _mqtt_logger_name = None
    _min_log_level = None

    def __init__(self, name='', mqtt_logger_name=None, min_log_level=None):
        if mqtt_logger_name is None or mqtt_logger_name=='':
            raise ValueError("mqtt_logger_name must be set")
        if min_log_level is None or min_log_level=='':
            raise ValueError("min_log_level must be set")
        self._mqtt_logger_name = mqtt_logger_name
        self._min_log_level = get_log_level(min_log_level)
        logging.Filter.__init__(self, name)

    def filter(self, record):
        if record.name.startswith(self._mqtt_logger_name):
            if record.level < self._min_log_level:
                return False
        return True
