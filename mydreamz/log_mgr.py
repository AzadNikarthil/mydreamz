import logging.config

import mydreamz.constant as CONSTANT

class LogMgr:
    """
    """

    def __init__(self):
        """
        """
        logging.config.fileConfig(CONSTANT.LOGGER_CONF,
                          disable_existing_loggers=False)

    def get_logger(self, name):
        """
        """
        return logging.getLogger(name)
