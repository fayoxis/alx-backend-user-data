#!/usr/bin/env python3
"""
Module for filtering and logging sensitive data.
Provides functions to redact PII, interact with a database,
and log user information securely. Includes custom formatter.
"""
import os
import re
import logging
import mysql.connector
from typing import List


patterns = {
    'extract': lambda x, y: r'(?P<field>{})=[^{}]*'.format('|'.join(x), y),
    'replace': lambda x: r'\g<field>={}'.format(x),
}
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str,
        ) -> str:
    """
    Redacts specified fields in a log message.
    Takes fields to redact, redaction string, original message,
    and field separator. Returns filtered message.
    """
    extract, replace = (patterns["extract"], patterns["replace"])
    return re.sub(extract(fields, separator), replace(redaction), message)


def get_logger() -> logging.Logger:
    """
    Sets up and returns a configured logger for user data.
    Includes a custom formatter to redact sensitive information.
    Uses StreamHandler for output.
    """
    logger = logging.getLogger("user_data")
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Establishes and returns a connection to the MySQL database.
    Uses environment variables for connection details like host,
    database name, username, and password.
    """
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME", "")
    db_user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_pwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    connection = mysql.connector.connect(
        host=db_host,
        port=3306,
        user=db_user,
        password=db_pwd,
        database=db_name,
    )
    return connection


def main():
    """
    Main function to retrieve user records from the database and
    log them securely. Demonstrates the use of the custom logger
    and database connection. Processes each row and creates a log
    record with sensitive information redacted.
    """
    fields = "name,email,phone,ssn,password,ip,last_login,user_agent"
    columns = fields.split(',')
    query = "SELECT {} FROM users;".format(fields)
    info_logger = get_logger()
    connection = get_db()
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        i = 0
        while i < len(rows):
            row = rows[i]
            record = []
            j = 0
            while j < len(columns):
                record.append('{}={}'.format(columns[j], row[j]))
                j += 1
            msg = '{};'.format('; '.join(record))
            args = ("user_data", logging.INFO, None, None, msg, None, None)
            log_record = logging.LogRecord(*args)
            info_logger.handle(log_record)
            i += 1


class RedactingFormatter(logging.Formatter):
    """
    Custom logging formatter that redacts specified fields.
    Inherits fromlogging.Formatter and overrides the format
    method to apply redaction.
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    FORMAT_FIELDS = ('name', 'levelname', 'asctime', 'message')
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats the log record, applying redaction to specified fields.
        Takes a LogRecord as input and returns a formatted
        and redacted log message string.
        """
        msg = super(RedactingFormatter, self).format(record)
        txt = filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)
        return txt


if __name__ == "__main__":
    main()
