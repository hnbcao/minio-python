import time

from flask import Flask, request

from minio_bridge import MinioBridge

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'upload/'
minioClient = MinioBridge('minio.segma.tech',
                          access_key='AKIAIOSFODNN7EXAMPLE',
                          secret_key='wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
                          secure=False)
bucket = 'flink-status'
# objectName = 'img3.png'
# filePath = 'img.png'


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/upload', methods=['POST'])
def uploader():
    if request.method == 'POST':
        # 501202
        file = request.files['file']
        now = time.time()
        objectName = '{0}-{1}'.format(str(round(now * 1000)), file.filename)
        minioClient.put_small_object(bucket, objectName, file, file.content_type)
        return 'file uploaded successfully'


if __name__ == '__main__':
    app.run()
