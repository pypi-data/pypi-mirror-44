class AbstractException(Exception):
    """Abstract exception for project"""

    def __init__(self, code, message):
        """
        Constructor

        :param int code: error code
        :param str message: error message
        """
        self._code = code
        self._message = message

    @property
    def code(self):
        """
        Getter code

        :rtype: int
        """
        return self._code

    @property
    def message(self):  # pragma no cover
        """
        Getter message

        :rtype: str
        """
        return self._message
