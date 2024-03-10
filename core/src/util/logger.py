import logging
import os
import datetime
import util.config as config

class Logger:
    _instance = None
    FRAME_LEVEL_NUM = 5
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.log_format = '%(asctime)s [%(levelname)s] %(message)s'
        self.log_dir = config.value_of('log_dir')
        self.log_level = config.value_of('log_level')
        self._create_log_dir()
        self._configure_logger()

    def _create_log_dir(self):
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    def _configure_logger(self):
        logging.basicConfig(format=self.log_format)
        logging.addLevelName(self.FRAME_LEVEL_NUM, "FRAME")
        self.logger = logging.getLogger()
        self.logger.setLevel(self.log_level)
        date = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        fh = logging.FileHandler(filename=f'{self.log_dir}/{date}.log', encoding='utf-8')
        formatter = logging.Formatter(self.log_format)
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

logger = Logger().logger

def debug(msg):
    logger.debug(msg)

def info(msg):
    logger.info(msg)

def warning(msg):
    logger.warning(msg)

def error(msg):
    logger.error(msg)

def critical(msg):
    logger.critical(msg)

def frame(message, args = None, **kwargs):
    if logger.isEnabledFor(Logger.FRAME_LEVEL_NUM):
        logger._log(Logger.FRAME_LEVEL_NUM, message, args, **kwargs)
