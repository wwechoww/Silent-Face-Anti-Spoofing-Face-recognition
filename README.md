# 人脸防伪和检测系统
 欢迎使用人脸防伪和检测系统！本项目基于小视科技的开源代码，原项目地址：https://github.com/minivision-ai/Silent-Face-Anti-Spoofing。

 该系统通过接收 RabbitMQ 消息来控制算法的开启和关闭。在算法运行时，系统通过 RabbitMQ 消息中的摄像头 URL 进行人脸检测，首先判断是否为真人，然后进行防伪检测，最终识别出人物并将检测结果保存到 Minio 对象存储中，同时发送具体信息到 RabbitMQ。

# 功能特性
 动态算法控制： 通过 RabbitMQ 消息动态控制人脸检测算法的开启和关闭。

 实时人脸检测： 根据 RabbitMQ 消息中的摄像头 URL 进行实时人脸检测。

 真人判断： 在检测到人脸后，进行真人判断，防止虚假人脸欺骗。

 防伪检测： 使用小视科技的防伪检测算法，提高人脸识别的准确性。

 人物识别： 进一步识别人物，并将检测图片结果保存到 Minio 对象存储中。

 消息通知： 向 RabbitMQ 发送具体信息，实现系统状态的实时通知。

对象存储： 将人脸检测结果保存到 Minio 中，便于检索和管理。

# 使用说明

 ## 替换人脸检测模型
 将 `trained_knn_model.clf` 替换为自己训练好的人脸检测模型。

 ## 配置 Minio
 替换 `minio_modules/minio_configs.py` 中的配置为自己的 Minio 对象存储信息。

 ## 配置 RabbitMQ
 替换 `rabbit_mq/rabbit_mq_config.py` 中的配置为自己的 RabbitMQ 信息。

# 快速开始
 ## 1.克隆项目：
 `git clone https://github.com/your_username/your_project.git`
 ## 2.替换模型和配置文件
 ## 3.安装依赖：
 `pip install -r requirements.txt`
 ## 4.运行系统
 `python start.py`

