import pika

# 建立到RabbitMQ服务器的连接
# RabbitMQ服务器的远程地址
rabbitmq_host = '42.192.42.17'
rabbitmq_port = 11992  # 默认端口号是5672

# RabbitMQ的用户名和密码
rabbitmq_username = '1198006606'
rabbitmq_password = 'Yby@17625207472'

# 建立到RabbitMQ服务器的连接
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=rabbitmq_host,
        port=rabbitmq_port,
        credentials=pika.PlainCredentials(username=rabbitmq_username, password=rabbitmq_password)
    )
)

channel = connection.channel()

def get_channel():
    try:

        return channel
    except Exception as e:
        print(f"Error creating channel: {e}")
        return None
