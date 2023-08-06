from unittest import TestCase
from photospicker.uploader.uploaders.filesystem_uploader \
    import FilesystemUploader
from mock import MagicMock
from photospicker.exception.uploader_exception import UploaderException
import mock
import sys


class TestFilesystemUploader(TestCase):
    """Test class for FilesystemUploader"""

    @mock.patch('os.listdir')
    @mock.patch('os.path.isdir')
    def test_constructor_directory_not_found(self, is_dir_mock, listdir_mock):
        """
        Test that an exception is launched if the directory is not found

        :param MagicMock is_dir_mock: is_dir function mock
        :param MagicMock listdir_mock: listdir function mock
        """
        is_dir_mock.return_value = False

        with self.assertRaises(UploaderException) as cm:
            FilesystemUploader('/root/myfolder')

        is_dir_mock.assert_called_with('/root/myfolder')

        self.assertEqual(UploaderException.NOT_FOUND, cm.exception.code)

    @mock.patch('os.listdir')
    @mock.patch('os.path.isdir')
    def test_constructor_directory_not_empty(self, is_dir_mock, listdir_mock):
        """
        Test that an exception is launched if the directory is not empty

        :param MagicMock is_dir_mock: is_dir function mock
        :param MagicMock listdir_mock: listdir function mock
        """
        is_dir_mock.return_value = True
        listdir_mock.return_value = ['myfile']

        with self.assertRaises(UploaderException) as cm:
            FilesystemUploader('/root/myfolder')

        is_dir_mock.assert_called_with('/root/myfolder')
        listdir_mock.assert_called_with('/root/myfolder')

        self.assertEqual(UploaderException.NOT_EMPTY, cm.exception.code)

    @mock.patch('os.listdir')
    @mock.patch('os.path.isdir')
    def test_upload(self, is_dir_mock, listdir_mock):
        """
        Test upload (copy)

        :param MagicMock is_dir_mock: is_dir function mock
        :param MagicMock listdir_mock: listdir function mock
        """
        is_dir_mock.return_value = True
        listdir_mock.return_value = []

        handle = MagicMock()

        builtin = '__builtin__' if sys.version_info < (3, 0) else 'builtins'

        with mock.patch(builtin + '.open') as mock_open:
            mock_open.return_value = handle

            sut = FilesystemUploader('/root/myfolder')
            sut.initialize()
            sut.upload('mydata', 'myphoto.jpg')

            path = '/root/myfolder/photo0.jpg'
            mock_open.assert_called_once_with(path, 'w+b')
        handle.__enter__().write.assert_called_once_with('mydata')
