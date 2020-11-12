from threading import Thread
# Import MinIO library.

from minio import Minio
from minio.error import InvalidArgumentError

# Constants
from minio.helpers import is_valid_sse_object, is_valid_bucket_name, is_non_empty_string, amzprefix_user_metadata

MAX_MULTIPART_COUNT = 10000  # 10000 parts
MAX_MULTIPART_OBJECT_SIZE = 5 * 1024 * 1024 * 1024 * 1024  # 5TiB
MAX_PART_SIZE = 5 * 1024 * 1024 * 1024  # 5GiB
MAX_POOL_SIZE = 10
MIN_PART_SIZE = 5 * 1024 * 1024  # 5MiB
DEFAULT_PART_SIZE = MIN_PART_SIZE * 2  # Currently its 5MiB


# Initialize minioClient with an endpoint and access/secret keys.
# 初始化minio客户端，设置minio地址与认证信息。access_key、secret_key为minio认证
# secure：是否使用https
# minioClient = Minio('minio.segma.tech',
#                     access_key='AKIAIOSFODNN7EXAMPLE',
#                     secret_key='wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
#                     secure=False)
#
# # Put an object 'pumaserver_debug.log' with contents from 'pumaserver_debug.log'.
# # bucket：存储桶，相当于文件夹的意思
# # objectName：对象名，minio中存储的对象名，相当于在minio中的文件名
# # filePath：待上传文件地址。
#
# bucket = 'flink-status'
# objectName = 'img2.png'
# filePath = 'img.png'


class MinioBridge:
    def __init__(self, endpoint, access_key=None,
                 secret_key=None,
                 session_token=None,
                 secure=True,
                 region=None,
                 http_client=None,
                 credentials=None):
        self._client = Minio(endpoint, access_key,
                             secret_key,
                             session_token,
                             secure,
                             region,
                             http_client,
                             credentials)

    def put_small_object(self, bucket_name, object_name, data,
                         content_type='application/octet-stream',
                         metadata=None, sse=None, progress=None,
                         part_size=DEFAULT_PART_SIZE):

        """
        Uploads data from a stream to an object in a bucket.
        上传文件至bucket中，方法通过改造Minio 的 put_object方法实现，不支持大文件上传。
        其中part_size指定文件限制，默认限制为10M，最小不少于5M，最大不能超过5GB

        :param bucket_name: Name of the bucket.
        :param object_name: Object name in the bucket.
        :param data: Contains object data.
        :param content_type: Content type of the object.
        :param metadata: Any additional metadata to be uploaded along
            with your PUT request.
        :param sse: Server-side encryption.
        :param progress: A progress object
        :param part_size: Multipart part size
        :return: etag and version ID if available.

        Example::
            file_stat = os.stat('hello.txt')
            with open('hello.txt', 'rb') as data:
                minio.put_object(
                    'foo', 'bar', data, file_stat.st_size, 'text/plain',
                )
        """
        is_valid_sse_object(sse)
        is_valid_bucket_name(bucket_name, False)
        is_non_empty_string(object_name)

        if not callable(getattr(data, 'read')):
            raise ValueError(
                'Invalid input data does not implement'
                ' a callable read() method')
        current_data = data.read()
        length = len(current_data)

        if progress:
            if not isinstance(progress, Thread):
                raise TypeError('Progress object should inherit the thread.')
            # Set progress bar length and object name before upload
            progress.set_meta(total_length=length, object_name=object_name)

        if length > part_size:
            raise InvalidArgumentError('Part size is lesser than input length.')

        if part_size < MIN_PART_SIZE:
            raise InvalidArgumentError('Input part size is smaller '
                                       ' than allowed minimum of 5MiB.')

        if part_size > MAX_PART_SIZE:
            raise InvalidArgumentError('Input part size is bigger '
                                       ' than allowed maximum of 5GiB.')

        if not metadata:
            metadata = {}

        metadata = amzprefix_user_metadata(metadata)
        metadata['Content-Type'] = content_type or 'application/octet-stream'

        # current_data = data.read(length)
        if len(current_data) != length:
            raise InvalidArgumentError(
                'Could not read {} bytes from data to upload'.format(length)
            )

        return self._client._do_put_object(bucket_name, object_name,
                                           current_data, len(current_data),
                                           metadata=metadata, sse=sse,
                                           progress=progress)
