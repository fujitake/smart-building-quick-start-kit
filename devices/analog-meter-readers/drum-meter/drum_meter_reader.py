import datetime
import json
import os
import time

import cv2
import numpy as np
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
from paddleocr import PaddleOCR, draw_ocr

load_dotenv()


def post_sensing_value(sensing_value):
    body = json.dumps(
        {
            "sensorId": "gasMeter001",
            "sensing_value": sensing_value,
            "timestamp": int(time.mktime(datetime.datetime.now().timetuple())),
        }
    )

    client = mqtt.Client()
    client.username_pw_set(os.getenv("MQTT_USER"), password=os.getenv("MQTT_PASSWORD"))
    client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLSv1_2, ciphers=None)
    client.tls_insecure_set(True)
    client.connect(os.getenv("MQTT_BROKER_HOST"), 8883)
    client.publish(os.getenv("MQTT_TOPIC"), body)
    client.disconnect()


def save_frame_camera(cap):
    _, frame = cap.read()
    return frame


def read_meter(frame):
    cv2.imwrite("./tmp/image.png", frame)
    ocr_target = "./tmp/ocr_target.png"

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Invert color (black text is more accurate for OCR)
    # If the text is originally white, do not invert it.
    invert_img = cv2.bitwise_not(gray)

    # Flatten the histogram
    hist_img = cv2.equalizeHist(invert_img)
    cv2.imwrite(ocr_target, hist_img)

    # OCR
    ocr = PaddleOCR(lang="en", use_gpu=False)
    result = ocr.ocr(ocr_target)

    if len(result) == 0:
        return None

    # Calculate area from Bbox
    acreage = []
    for row in result:
        x = row[0][2][0] - row[0][0][0]
        y = row[0][2][1] - row[0][0][1]
        acreage.append(x * y)

    # Return the value of the object with the largest area
    index = np.argmax(acreage)
    return result[index][1][0]


cap = cv2.VideoCapture(0)
time.sleep(3)


while True:
    frame = save_frame_camera(cap)
    # If want to you use a sample image, please uncomment the following line:
    # frame = cv2.imread("./img/sample.jpg")

    sensing_value = read_meter(frame)
    print(f"Sensing value: {sensing_value}.")

    if sensing_value:
        post_sensing_value(sensing_value)

    time.sleep(30)
