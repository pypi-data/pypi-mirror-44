from photospicker.exception.abstract_exception import AbstractException


class UploaderException(AbstractException):
    """Exception when uploading photos"""

    # Error constants
    NOT_FOUND = 1
    NOT_EMPTY = 2
    MANY_DIRS = 3
    INVALID_DIR_NAME = 4
