import os

from azure.storage.blob import BlobServiceClient, ContainerClient


CONNECTING_STR = 'DefaultEndpointsProtocol=https;AccountName=ca4adintsharedhdinsight;AccountKey=ZUDkD8U8rpvcVIIg4a2xhEh0uZjhn6YLnXs1dOfhxCtTNos7TY4AG1M9jsJl7n8fwKkzGbvGEqAD6regaPp8bQ==;EndpointSuffix=core.chinacloudapi.cn'

CONTAINER = '''https://ca4adintsharedhdinsight.blob.core.chinacloudapi.cn/ca4ad-int-hdinsight-spa-2021-11-29t09-24-11
-903z?sp=racwdl&st=2022-03-09T01:40:58Z&se=2022-03-13T09:40:58Z&spr=https&sv=2020-08-04&sr=c&sig=VZoANJkYY798RrnNvl
%2FfYYOokjQ33JD6vVWoTiDM0RE%3D'''


class StorageClient:
    def __init__(self, container_name):
        service_client = BlobServiceClient.from_connection_string(CONNECTING_STR)
        self.client = service_client.get_container_client(container_name)
        self.client1 = ContainerClient.from_container_url(CONTAINER)

    def ls_files(self, path, recursive=False):
        if not path == '' and not path.endswith('/'):
            path += '/'

        blob_iter = self.client.list_blobs(name_starts_with=path)
        files = []
        for blob in blob_iter:
            relative_path = os.path.relpath(blob.name, path)
            if recursive or '/' not in relative_path:
                files.append(relative_path)

        return files

    def ls_dirs(self, path, recursive=False):
        if not path == '' and not path.endswith('/'):
            path += '/'

        blob_iter = self.client.list_blobs(name_starts_with=path)
        dirs = []
        for blob in blob_iter:
            relative_dir = os.path.dirname(os.path.relpath(blob.name, path))
            if relative_dir and (recursive or '/' not in relative_dir) and relative_dir not in dirs:
                dirs.append(relative_dir)

        return dirs

    def upload(self, source, target):
        """
        Upload a file or directory to a path inside the container
        """
        if os.path.isdir(source):
            self.upload_dir(source, target)
        else:
            self.upload_file(source, target)

    def upload_file(self, source, target):
        """
        Upload a single file to a path inside the container
        """
        print(f'Uploading {source} to {target}')
        with open(source, 'rb') as data:
            self.client.upload_blob(name=target, data=data)

    def upload_dir(self, source, target):
        """
        Upload a directory to a path inside the container
        """
        prefix = '' if target == '' else target + '/'
        prefix += os.path.basename(source) + '/'
        for root, dirs, files in os.walk(source):
            for name in files:
                dir_part = os.path.relpath(root, source)
                dir_part = '' if dir_part == '.' else dir_part + '/'
                file_path = os.path.join(root, name)
                blob_path = prefix + dir_part + name
                self.upload_file(file_path, blob_path)

    def rm(self, path, recursive=False):
        """
        Remove a single file, or remove a path recursively
        """
        if recursive:
            self.rmdir(path)
        else:
            print(f'Deleting {path}')
            self.client.delete_blob(path)

    def rmdir(self, path):
        """
        Remove a directory and its contents recursively
        """
        blobs = self.ls_files(path, recursive=True)
        if not blobs:
            return

        if not path == '' and not path.endswith('/'):
            path += '/'
        blobs = [path + blob for blob in blobs]
        print(f'Deleting {", ".join(blobs)}')
        self.client.delete_blobs(*blobs)

    def download(self, source, dest):
        """
        Download a file or directory to a path on the local filesystem
        """
        if not dest:
            raise Exception('A destination must be provided')

        blobs = self.ls_files(source, recursive=True)
        if blobs:
            # if source is a directory, dest must also be a directory
            if not source == '' and not source.endswith('/'):
                source += '/'
            if not dest.endswith('/'):
                dest += '/'
            # append the directory name from source to the destination
            dest += os.path.basename(os.path.normpath(source)) + '/'

            blobs = [source + blob for blob in blobs]
            for blob in blobs:
                blob_dest = dest + os.path.relpath(blob, source)
                self.download_file(blob, blob_dest)
        else:
            self.download_file(source, dest)

    def download_file(self, source, dest):
        """
        Download a single file to a path on the local filesystem
        """
        # dest is a directory if ending with '/' or '.', otherwise it's a file
        if dest.endswith('.'):
            dest += '/'
        blob_dest = dest + os.path.basename(source) if dest.endswith('/') else dest

        print(f'Downloading {source} to {blob_dest}')
        os.makedirs(os.path.dirname(blob_dest), exist_ok=True)
        bc = self.client.get_blob_client(blob=source)
        with open(blob_dest, 'wb') as file:
            data = bc.download_blob()
            file.write(data.readall())

    def get_policy(self):
        print(self.client.get_container_access_policy())


if __name__ == '__main__':
    cli = StorageClient('fap5ea')
    file_ls = cli.ls_files('FAP5/data/incidents/year=2022/month=3/day=10')  # spark/streaming/fap5ea
    print(len(file_ls))
    # download
    # num = 1
    # for file in file_ls:
    #     if file.endswith('.parquet'):
    #         file_path = os.path.join('FAP5/data/incidents/year=2022/month=3/day=9/', file)
    #         dest_file_name = os.path.join('FAP5/data/incidents/year=2022/month=3/day=9/', str(num) + '.parquet')
    #         cli.download_file(file_path, dest_file_name)
    #         num += 1

    # del
    for file in file_ls[0:250]:
        file_path = os.path.join('FAP5/data/incidents/year=2022/month=3/day=10', file)
        cli.rm(file_path)
