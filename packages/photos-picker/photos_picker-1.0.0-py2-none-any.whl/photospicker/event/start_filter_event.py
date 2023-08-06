from photospicker.filter.abstract_filter import AbstractFilter  # noqa


class StartFilterEvent(object):
    """Event dispatched before a filter execution"""

    def __init__(self, photo_filter, filepath):
        """
        Constructor

        :param AbstractFilter photo_filter: filter
        :param str filepath: file processed by the filter
        """
        self._filter_name = photo_filter.__class__.__name__
        self._filepath = filepath

    def filter_name(self):  # pragma: no cover
        """
        Getter for the filter name

        :rtype: str
        """
        return self._filter_name

    def filepath(self):  # pragma: no cover
        """
        Getter for the file path of the processes file

        :rtype: str
        """
        return self._filepath
