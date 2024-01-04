from datetime import datetime
import cv2
import json
import subprocess
import pytz
import minio_configs
from rabbit_mq.algorithm_message_vo import AlgRush
from rabbit_mq.rabbit_mq_config import get_channel


def create_transport(camera_url, upload_url):

    # 打开 RTSP 视频流
    if(camera_url=="0"):
        cap = cv2.VideoCapture(0)
    else:
        cap = cv2.VideoCapture(camera_url)

    # 检查摄像头是否成功打开
    if not cap.isOpened():
        print("Error: Could not open RTSP stream.")
        exit()

    # 读取一帧来获取视频的宽度和高度
    ret, frame = cap.read()

    # 检查是否成功读取帧
    if not ret:
        print("Error: Could not read frame.")
        exit()

    # 获取视频的宽度和高度
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    sizeStr = str(width) + 'x' + str(height)
    command = ['ffmpeg',
               '-y', '-an',
               '-f', 'rawvideo',
               '-vcodec', 'rawvideo',
               '-pix_fmt', 'bgr24',
               '-s', sizeStr,
               '-r', '25',
               '-i', '-',
               '-c:v', 'libx264',
               '-pix_fmt', 'yuv420p',
               '-preset', 'ultrafast',
               '-f', 'flv',
               upload_url]
    pipe = subprocess.Popen(command, shell=False, stdin=subprocess.PIPE)
    # 释放资源
    cap.release()
    return pipe


def send_mq_message(algorithm_command, image_url, result_text, name):
    illegal = 1 if name is None or name == "unknown" else 0
    image_url = "http://" + minio_configs.minio_config.endpoint + "/" + minio_configs.minio_config.bucket + "/" + image_url

    # 获取当前时间并指定时区为UTC
    current_datetime_utc = datetime.now(pytz.utc)
    beijing_timezone = pytz.timezone('Asia/Shanghai')
    current_datetime_beijing = current_datetime_utc.astimezone(beijing_timezone)

    # 格式化时间
    formatted_datetime = current_datetime_beijing.strftime("%Y-%m-%d %H:%M:%S")
    print("send_time:" + formatted_datetime)

    mq_message = AlgRush(
        cameraUrl=algorithm_command.cameraUrl,
        cameraName=algorithm_command.cameraName,
        userName=name,
        checkTime=formatted_datetime,
        illegal=illegal,
        message=result_text,
        imgUrl=image_url
    )
    message_body = json.dumps(mq_message.to_dict())

    # 创建一个通道
    send_message_channel = get_channel()

    # 将消息发布到队列
    send_message_channel.basic_publish(exchange='algorithm-event-exchange', routing_key='algorithm.rush.message', body=message_body)
