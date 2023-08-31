#!/usr/bin/env python3
"""
Created by Jenaide Sibolie
"""
import os
import re
from typing import List
import logging


patterns = {
    'extract': lambda x, y: r'(?P<field>{})=[^{}]*'.format('|'.join(x), y),
    'replace': lambda x: r'\g<field>={}'.format(x),
}
PII_FIELDS = ("name", "email", "phone", "ssn", "password")



def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    a fuction that returns the log message abfuscated
    """
    extract, replace = (patterns['extract'], patterns['replace'])
    return re.sub(extract(fields, separator), replace(redaction), message)


def get_logger() -> logging.Logger:
    """
    function that creates a new log for user data
    """
    logger = logging.getLogger("user_data")
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.addHandler(handler)
    return logger


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    FORMAT_FIELDS = ('name', 'levelname', 'asctime', 'message')
    SEPARATOR = ";"

    def __init__(self, fields):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        LogRecord formatter
        """
        message = super(RedactingFormatter, self).format(record)
        text = filter_datum(self.fields, self.REDACTION, message, self.SEPARATOR)
        return text
