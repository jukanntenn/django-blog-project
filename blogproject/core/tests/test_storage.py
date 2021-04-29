import io
import unittest
from unittest import mock

from core.storage import TencentCOSStorage
from django.core.files.base import File
from qcloud_cos.cos_exception import CosServiceError


class TecentCOSStorageTestCase(unittest.TestCase):
    def setUp(self):
        self.storage = TencentCOSStorage(
            options={
                "BUCKET": "test-bucket",
                "REGION": "ap-beijing",
                "SECRETID": "secretid",
                "SECRETKEY": "secretkey",
            }
        )

    @mock.patch("qcloud_cos.CosS3Client.delete_object", return_value=None)
    def test_delete(self, *args):
        self.assertIsNone(self.storage.delete("test.file"))

    @mock.patch("qcloud_cos.CosS3Client.head_object", return_value={"foo": "bar"})
    def test_exists(self, *args):
        self.assertTrue(self.storage.exists("test.file"))

    @mock.patch(
        "qcloud_cos.CosS3Client.head_object",
        side_effect=CosServiceError(
            method="", message={"code": "NoSuchResource"}, status_code=404
        ),
    )
    def test_doesnot_exists(self, *args):
        self.assertFalse(self.storage.exists("nonexistence.file"))

    @mock.patch(
        "qcloud_cos.CosS3Client.head_object",
        side_effect=CosServiceError(
            method="", message={"code": "Denied"}, status_code=403
        ),
    )
    def test_exists_raise_exception(self, *args):
        with self.assertRaises(CosServiceError):
            self.storage.exists("test.file")

    @mock.patch(
        "qcloud_cos.CosS3Client.list_objects",
        return_value={
            "Contents": [
                {"Key": "dir1/"},
                {"Key": "dir2/"},
                {"Key": "file1"},
                {"Key": "file2"},
            ],
            "IsTruncated": "false",
        },
    )
    def test_listdir_not_truncated(self, *args):
        dirs, files = self.storage.listdir("")
        self.assertListEqual(dirs, ["dir1/", "dir2/"])
        self.assertListEqual(files, ["file1", "file2"])

    @mock.patch(
        "qcloud_cos.CosS3Client.list_objects",
        side_effect=[
            {
                "Contents": [
                    {"Key": "dir1/"},
                    {"Key": "file1"},
                ],
                "IsTruncated": "true",
                "NextMarker": 2,
            },
            {
                "Contents": [
                    {"Key": "dir2/"},
                    {"Key": "file2"},
                ],
                "IsTruncated": "false",
            },
        ],
    )
    def test_listdir_truncated(self, mock_list_objects):
        dirs, files = self.storage.listdir("")
        self.assertListEqual(dirs, ["dir1/", "dir2/"])
        self.assertListEqual(files, ["file1", "file2"])
        self.assertEqual(mock_list_objects.call_count, 2)

    @mock.patch(
        "qcloud_cos.CosS3Client.head_object",
        return_value={"Content-Length": 10},
    )
    def test_size(self, *args):
        self.assertEqual(self.storage.size("test.file"), 10)

    def test_modified_time_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.assertEqual(self.storage.get_modified_time("test.file"))

    def test_accessed_time_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.assertEqual(self.storage.get_accessed_time("test.file"))

    def test__open(self, *args):
        obj = self.storage._open("file")
        self.assertIsInstance(obj, File)

    @mock.patch("qcloud_cos.CosS3Client.upload_file_from_buffer", return_value=None)
    def test__save(self, mock_upload_file_from_buffer):
        self.storage._save("file", File(io.BytesIO(b"bar"), "foo"))
        self.assertTrue(mock_upload_file_from_buffer.called)
