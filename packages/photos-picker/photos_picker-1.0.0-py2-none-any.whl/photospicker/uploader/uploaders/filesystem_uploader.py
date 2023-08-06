from photospicker.uploader.abstract_uploader import AbstractUploader
from photospicker.exception.uploader_exception import UploaderException
import os


class FilesystemUploader(AbstractUploader):
    """Copy picked photo to a filesystem empty directory"""

    def __init__(self, folder_path):
        """
        Constructor

        :param str folder_path: target folder path
        """
        super(FilesystemUploader, self).__init__(folder_path)

        """Check target directory"""
        if not os.path.isdir(self._path):
            raise UploaderException(
                UploaderException.NOT_FOUND,
                "Directory {path} not found".format(path=self._path)
            )

        if os.listdir(self._path):
            raise UploaderException(
                UploaderException.NOT_EMPTY,
                "Directory {path} not empty".format(path=self._path)
            )

    def initialize(self):
        pass

    def upload(self, binary, original_filename):
        """
        Upload or copy files to destination

        :param str binary: binary data to upload
        :param str original_filename: original file name
        """
        filename = self._build_filename(original_filename)
        with open(os.path.join(self._path, filename), 'w+b') as f:
            f.write(binary)
