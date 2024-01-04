import json
import threading
from rush import start
from globala_vars import global_variable_list
from rabbit_mq.algorithm_command_vo import AlgorithmCommandVo
from rush_utils import create_transport

def callback(ch, method, properties, body):
    # 接收到消息时的回调函数
    json_message = body.decode('utf-8')

    try:
        # 尝试将JSON字符串解析为Python对象
        json_data = json.loads(json_message)

        # 创建AlgorithmCommandVo对象
        algorithm_command = AlgorithmCommandVo(**json_data)
        # 处理解析后的消息
        process_algorithm_command(algorithm_command)

    except Exception as e:
        print("Error parsing or processing message:", str(e))

def process_algorithm_command(algorithm_command):
    # 在这里添加对消息的具体处理逻辑
    print("Received AlgorithmCommand:")
    print("Camera URL:", algorithm_command.cameraUrl)
    print("Camera Name:", algorithm_command.cameraName)
    print("Upload URL:", algorithm_command.uploadUrl)
    print("Enable:", algorithm_command.enable)
    print("-------------------------")

    pipe = create_transport(algorithm_command.cameraUrl, algorithm_command.uploadUrl)
    if algorithm_command.enable == 1:
        # 启动代码块

        start_thread = threading.Thread(target=start_algorithm, args=(pipe, algorithm_command))
        start_thread.start()
    elif algorithm_command.enable == 0:
        # 停止代码块
        stop_thread = threading.Thread(target=stop_algorithm)
        stop_thread.start()
        pipe.terminate()
    else:
        print("Invalid value for 'enable'. Expected 0 or 1.")
        pipe.terminate()

# 启动算法的代码块
def start_algorithm(pipe, algorithm_command):
    print("Starting algorithm...")
    model_dir = "./resources/anti_spoof_models"
    device_id = 0
    global_variable_list['running_tag'] = 1
    start(pipe, algorithm_command, model_dir, device_id)
    print("algorithm finished")


def stop_algorithm():
    print("Stopping algorithm...")
    global_variable_list['running_tag'] = 0
    print("stop finished")
