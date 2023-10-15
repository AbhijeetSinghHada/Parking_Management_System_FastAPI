import logging


def setup_logger(log_file):
    """Function to setup the logger"""

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename=log_file,)
    return logging.getLogger()


def get_logger(name):
    return logging.getLogger(name)


def log_info(logger, info_message):
    logger.info(info_message)


def log_debug(logger, debug_message):
    logger.debug(debug_message)


def log_warning(logger, warning_message):
    logger.warning(warning_message)


def log_error(logger, error_message):
    logger.error(error_message)


def log_critical(logger, critical_message):
    logger.critical(critical_message)
