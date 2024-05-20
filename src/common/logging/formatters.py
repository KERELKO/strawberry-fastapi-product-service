import logging


class SimpleFormatter(logging.Formatter):
    def format(self, record):
        return f'{record.levelname}: {record.message}'
