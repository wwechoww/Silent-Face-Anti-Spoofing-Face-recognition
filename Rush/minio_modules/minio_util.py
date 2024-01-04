import os
from io import BytesIO
import cv2
from minio import Minio
from minio.error import InvalidResponseError
from datetime import datetime
from minio_configs import minio_config
minio_endpoint = minio_config.endpoint
minio_access_key = minio_config.access_key
minio_secret_key = minio_config.secret_key
minio_bucket = minio_config.bucket

minio_client = Minio(minio_endpoint, access_key=minio_access_key, secret_key=minio_secret_key, secure=False)

def upload_image(file_path):
    # 获取当前日期
    current_date = datetime.now()
    year = current_date.year
    month = current_date.month
    day = current_date.day

    # 构建对象名称
    object_name = f"{year}/{month}/{day}/{os.path.basename(file_path)}"

    try:
        # 检查桶是否存在，不存在则创建
        if not minio_client.bucket_exists(minio_bucket):
            minio_client.make_bucket(minio_bucket)

        # 上传文件
        minio_client.fput_object(minio_bucket, object_name, file_path)

        print(f"Image uploaded successfully to {object_name}")
        return object_name  # 返回上传后的对象名称
    except InvalidResponseError as err:
        print(f"MinIO Error: {err}")
        return None

def upload_frame(frame):
    # 获取当前时间信息
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    minute = now.minute
    second = now.second

    # 构建文件夹路径和文件名
    folder_path = f"{year}/{month}/{day}"
    file_name = f"{hour}-{minute}-{second}.jpg"

    # 将帧转换为字节流
    _, buffer = cv2.imencode(".jpg", frame)
    image_bytes = BytesIO(buffer.tobytes())

    # 上传帧到MinIO
    image_url = f"{folder_path}/{file_name}"
    try:
        minio_client.put_object(minio_bucket, image_url, image_bytes, len(image_bytes.getvalue()), content_type="image/jpeg")
        print(f"Image uploaded successfully to {image_url}")
        return image_url  # 返回上传后的对象名称
    except InvalidResponseError as err:
        print(f"MinIO Error: {err}")
        return None