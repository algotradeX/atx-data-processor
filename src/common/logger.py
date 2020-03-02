# coding: utf-8

import logging
from logging.handlers import TimedRotatingFileHandler
from src.common import Singleton
from dynaconf import settings
import sys

import os

FORMATTER = logging.Formatter("%(asctime)s  %(levelname)s  %(message)s")
LOGGING_FILE_BASE_PATH = settings["LOGGING"]["basepath"]


class Logger(metaclass=Singleton):
    def __init__(self, name="logger"):
        self.logger = logging.getLogger(settings["APP_NAME"])
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(self.get_console_handler())
        self.logger.addHandler(self.get_file_handler())

    @staticmethod
    def check_create_base_folder():
        if not os.path.exists(LOGGING_FILE_BASE_PATH):
            os.makedirs(LOGGING_FILE_BASE_PATH)

    @staticmethod
    def get_console_handler():
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(FORMATTER)
        return console_handler

    def get_file_handler(self):
        self.check_create_base_folder()
        log_file = f"{LOGGING_FILE_BASE_PATH}/{settings['APP_NAME']}.log"
        file_handler = TimedRotatingFileHandler(log_file, when="midnight")
        file_handler.setFormatter(FORMATTER)
        return file_handler

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, e):
        self.logger.error(e, exc_info=True)

    def exception(self):
        return self.logger.exception
