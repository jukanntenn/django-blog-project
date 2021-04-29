from io import BytesIO

from django.conf import settings
from django.core.files.base import File
from django.core.files.storage import Storage
from django.utils._os import safe_join
from django.utils.deconstruct import deconstructible
from qcloud_cos import CosConfig, CosS3Client
from qcloud_cos.cos_exception import CosServiceError


class TencentCOSFile(File):
    def __init__(self, name, storage):
        self.name = name
        self._storage = storage
        self._file = None

    def _get_file(self):
        if self._file is None:
            response = self._storage.client.get_object(
                Bucket=self._storage.bucket,
                Key=self.name,
            )
            # type(raw_stream) is <class 'urllib3.response.HTTPResponse'>
            raw_stream = response["Body"].get_raw_stream()
            self._file = BytesIO(raw_stream.data)
            self._file.seek(0)
        return self._file

    def _set_file(self, value):
        self._file = value

    file = property(_get_file, _set_file)


@deconstructible
class TencentCOSStorage(Storage):
    """Tencent Cloud Object Storage class for Django pluggable storage system."""

    def __init__(self, options=None):
        if options is None:
            options = settings.TECENT_COS_OPTIONS

        self.bucket = options["BUCKET"]
        self.root_path = options.get("ROOT_PATH", "/")

        config = CosConfig(
            Region=options["REGION"],
            SecretId=options["SECRETID"],
            SecretKey=options["SECRETKEY"],
            Token=options.get("TOKEN"),
        )
        self.client = CosS3Client(config)

    def _full_path(self, name):
        if name == "/":
            name = ""
        return safe_join(self.root_path, name).replace("\\", "/")

    def delete(self, name):
        self.client.delete_object(Bucket=self.bucket, Key=self._full_path(name))

    def exists(self, name):
        try:
            return bool(
                self.client.head_object(Bucket=self.bucket, Key=self._full_path(name))
            )
        except CosServiceError as e:
            if e.get_status_code() == 404 and e.get_error_code() == "NoSuchResource":
                return False
            raise

    def listdir(self, path):
        directories, files = [], []
        full_path = self._full_path(path)

        if full_path == "/":
            full_path = ""

        contents = []
        marker = ""
        while True:
            # return max 1000 objects every call
            response = self.client.list_objects(
                Bucket=self.bucket, Prefix=full_path.lstrip("/"), Marker=marker
            )
            contents.extend(response["Contents"])
            if response["IsTruncated"] == "false":
                break
            marker = response["NextMarker"]

        for entry in contents:
            if entry["Key"].endswith("/"):
                directories.append(entry["Key"])
            else:
                files.append(entry["Key"])
        # directories includes path itself
        return directories, files

    def size(self, name):
        head = self.client.head_object(Bucket=self.bucket, Key=self._full_path(name))
        return head["Content-Length"]

    def get_modified_time(self, name):
        # Not implement now
        return super().get_modified_time(name)

    def get_accessed_time(self, name):
        # Not implement now
        return super().get_accessed_time(name)

    def url(self, name):
        return self.client.get_conf().uri(
            bucket=self.bucket, path=self._full_path(name)
        )

    def _open(self, name, mode="rb"):
        return TencentCOSFile(self._full_path(name), self)

    def _save(self, name, content):
        self.client.upload_file_from_buffer(
            Bucket=self.bucket, Key=self._full_path(name), Body=content
        )
        return name

    def get_available_name(self, name, max_length=None):
        name = self._full_path(name)
        return super().get_available_name(name, max_length)
