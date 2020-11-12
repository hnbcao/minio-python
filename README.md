# 使用指南

#### 一、安装minio

```shell script
pip install minio
```

#### 二、使用MinioBridge上传文件（针对无法获取流大小的情况），只能小文件（默认限制10M，最大不超过5GB）

```python
import time
from minio_bridge import MinioBridge
from minio import ResponseError

# 初始化minio
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
        result = minio.put_small_object(bucket, objectName, file, content_type)     
    except ResponseError as err:
        print(err)
```

#### 三、使用Minio上传文件（针对可以获取流大小的情况，文件大小无限制）

```python
import os
import time

from minio import Minio, ResponseError

# 初始化minio
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
    except ResponseError as err:
        print(err)

```