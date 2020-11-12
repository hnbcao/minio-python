import unittest
import time

from minio import ResponseError

from minio_bridge import MinioBridge


class MinioBridgeTestCase(unittest.TestCase):
    def test_something(self):
        minio = MinioBridge('minio.segma.tech',
                            access_key='AKIAIOSFODNN7EXAMPLE',
                            secret_key='wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
                            secure=False)
        filePath = 'img.png'
        bucket = 'flink-status'
        content_type = 'application/octet-stream'
        with open(filePath, 'rb') as file:
            objectName = '{0}-{1}'.format(str(round(time.time() * 1000)), filePath)
            """
            bucket: 存储桶
            objectName：对象名（minio中存储的对象名）
            file：文件流
            content_type：文件类型
            """
            try:
                minio.put_small_object(bucket, objectName, file, content_type)
                self.assertEqual(True, True)
            except ResponseError as err:
                print(err)
                self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
