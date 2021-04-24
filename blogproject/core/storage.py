from django_storage_qcloud.storage import QcloudStorage as BaseQcloudStorage


class QcloudStorage(BaseQcloudStorage):
    def listdir(self, path):
        directories, files = [], []

        result = self.client.list_objects(self.bucket)
        for entry in result["Contents"]:
            if entry.endswith("/"):
                directories.append(entry["Key"])
            else:
                files.append(entry["Key"])
        return directories, files
