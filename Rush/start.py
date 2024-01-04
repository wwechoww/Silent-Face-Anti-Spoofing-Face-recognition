from rabbit_mq.rabbit_mq_config import get_channel
from mq_receive_command import callback


# 创建一个通道
receive_message_channel = get_channel()

# 设置消息接收回调函数
receive_message_channel.basic_consume(queue='algorithm.rush.command.queue', on_message_callback=callback, auto_ack=True)

# 开始接收消息
print('Waiting for messages. To exit press CTRL+C')
receive_message_channel.start_consuming()