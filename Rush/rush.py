import os
import cv2
import numpy as np
import warnings
import pickle
import time
import threading
import face_recognition
from PIL import Image, ImageDraw, ImageFont
from src.anti_spoof_predict import AntiSpoofPredict
from src.generate_patches import CropImage
from src.utility import parse_model_name
from globala_vars import global_variable_list
from minio_modules.minio_util import upload_frame
from rush_utils import send_mq_message
warnings.filterwarnings('ignore')

def cv2ImgAddText(img, text, left, top, textColor=(0, 255, 0), textSize=20):
    if (isinstance(img, np.ndarray)):  # 判断是否OpenCV图片类型
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # 创建一个可以在给定图像上绘图的对象
    draw = ImageDraw.Draw(img)
    # 字体的格式
    fontStyle = ImageFont.truetype("font/simsun.ttc", textSize, encoding="utf-8")
    # 绘制文本
    draw.text((left, top), text, textColor, font=fontStyle)
    # 转换回OpenCV格式
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)


def predict(X_frame, knn_clf=None, model_path=None, distance_threshold=0.5):
    if knn_clf is None and model_path is None:
        raise Exception("Must supply knn classifier either thourgh knn_clf or model_path")

    # Load a trained KNN model (if one was passed in)
    if knn_clf is None:
        with open(model_path, 'rb') as f:
            knn_clf = pickle.load(f)

    X_face_locations = face_recognition.face_locations(X_frame)

    # If no faces are found in the image, return an empty result.
    if len(X_face_locations) == 0:
        return []

    # Find encodings for faces in the test image
    faces_encodings = face_recognition.face_encodings(X_frame, known_face_locations=X_face_locations)

    # Use the KNN model to find the best matches for the test face
    closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)
    are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(X_face_locations))]

    # Predict classes and remove classifications that aren't within the threshold

    return [(pred, loc) if rec else ("unknown", loc) for pred, loc, rec in
            zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)]

'''
常见网络摄像头，如海康威视，帧率为25fps
'''
def start(pipe, algorithm_command, model_dir, device_id):
    upload_tag = 0
    model_test = AntiSpoofPredict(device_id)
    image_cropper = CropImage()
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if global_variable_list['running_tag'] == 1:
            image = frame
            image_bbox = model_test.get_bbox(image)
            if image_bbox == [0, 0, 1, 1]:
                upload_tag = 0
            else:
                upload_tag += 1
            prediction = np.zeros((1, 3))
            test_speed = 0
            # sum the prediction from single model's result
            for model_name in os.listdir(model_dir):
                h_input, w_input, model_type, scale = parse_model_name(model_name)
                param = {
                    "org_img": image,
                    "bbox": image_bbox,
                    "scale": scale,
                    "out_w": w_input,
                    "out_h": h_input,
                    "crop": True,
                }
                if scale is None:
                    param["crop"] = False
                img = image_cropper.crop(**param)
                start = time.time()
                prediction += model_test.predict(img, os.path.join(model_dir, model_name))
                test_speed += time.time() - start
            # draw result of prediction
            label = np.argmax(prediction)
            value = prediction[0][label] / 2
            name = None
            if label == 1:
                # print("Real Face. Score: {:.2f}.".format(value))
                result_text = "真人 通过验证"
                color = (255, 0, 0)
                textColor = (0, 0, 255)
                predictions = predict(img, model_path="trained_knn_model.clf")
                if len(predictions) == 0:
                    result_text = "真人 无此人信息"
                    color = (0, 255, 255)
                    textColor = (255, 255, 0)
                for name, (top, right, bottom, left) in predictions:
                    if name == "unknown":
                        result_text = "真人 无此人信息"
                        textColor = (255, 255, 0)
            else:
                # print("is Fake Face. Score: {:.2f}.".format(value))
                result_text = "假人"
                color = (0, 0, 255)
                textColor = (255, 0, 0)
            cv2.rectangle(
                image,
                (image_bbox[0], image_bbox[1]),
                (image_bbox[0] + image_bbox[2], image_bbox[1] + image_bbox[3]),
                color, 2)
            image = cv2ImgAddText(image, result_text, left=int(image_bbox[0]), top=int(image_bbox[1] - 25),
                                  textColor=textColor, textSize=25)
            # 等待5帧画面稳定之后再保存
            if upload_tag == 5:
                upload_thread = threading.Thread(target=upload,
                                                 args=(image, algorithm_command, result_text, name), name='MyThread')
                # 启动线程
                upload_thread.start()

            pipe.stdin.write(image.tobytes())
        else:
            pipe.terminate()
            cap.release()
            break

def upload(frame, algorithm_command, result_text, name):
    image_url = upload_frame(frame)
    send_mq_message(algorithm_command, image_url, result_text, name)