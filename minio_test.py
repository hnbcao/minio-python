import os
import unittest
import time

from minio import Minio, ResponseError


class MinioTestCase(unittest.TestCase):
    def test_something(self):
        minio = Minio('minio.segma.tech',
                      access_key='AKIAIOSFODNN7EXAMPLE',
                      secret_key='wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
                      secure=False)
        filePath = 'img.png'
        bucket = 'flink-status'
        content_type = 'application/octet-stream'
        with open(filePath, 'rb') as file:
            file_size = os.stat(filePath).st_size
            object_name = '{0}-{1}'.format(str(round(time.time() * 1000)), filePath)
            """
            bucket: 存储桶
            object_name：对象名（minio中存储的对象名）
            file：文件流
            file_size：文件流大小
            content_type：文件类型
            """
            try:
                minio.put_object(bucket, object_name, file, file_size, content_type)
                self.assertEqual(True, True)
            except ResponseError as err:
                print(err)
                self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
