import datetime
import json
import os
import time

import cv2
import numpy as np
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

load_dotenv()

GREEN_START = 65
GREEN_END = 70

RED_START = 175
RED_END = 180


def resize_small(image):
    return cv2.resize(
        image, dsize=(0, 0), fx=0.2, fy=0.2, interpolation=cv2.INTER_LINEAR
    )


def extract_rough_led_image(image, h_start, h_end):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, _, _ = cv2.split(hsv)

    h = cv2.inRange(h, h_start, h_end)

    masked_image = cv2.bitwise_and(hsv, hsv, mask=h)

    return cv2.cvtColor(masked_image, cv2.COLOR_BGR2GRAY)


def clean_image(image):
    kernel = np.ones((20, 20), np.uint8)

    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)


def find_led_lamps(image):
    _, bin_img = cv2.threshold(image, 20, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(
        bin_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    return contours, hierarchy, bin_img


def post_sensing_value(sensing_value):
    body = json.dumps(
        {
            "sensor_id": "boiler001",
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


def detect_light(image, h_start, h_end):
    rough_img = extract_rough_led_image(image, h_start, h_end)
    clean_img = clean_image(rough_img)
    contours, _, _ = find_led_lamps(clean_img)

    return contours


def pick_led(cap):
    while True:
        _, frame = cap.read()

        green_contours = detect_light(frame, GREEN_START, GREEN_END)
        red_contours = detect_light(frame, RED_START, RED_END)

        if len(green_contours) > 0:
            print("Green is detected.")
            post_sensing_value("green")
        elif len(red_contours) > 0:
            print("Red is detected.")
            post_sensing_value("red")
        elif len(green_contours) <= 0 and len(red_contours) <= 0:
            print("Nothing is detected.")
        else:
            print("Both is detected.")

        time.sleep(30)


def testing_sample_img(frame):
    green_contours = detect_light(frame, GREEN_START, GREEN_END)
    red_contours = detect_light(frame, RED_START, RED_END)

    if len(green_contours) > 0:
        print("Green is detected.")
        post_sensing_value("green")
    elif len(red_contours) > 0:
        print("Red is detected.")
        post_sensing_value("red")
    elif len(green_contours) <= 0 and len(red_contours) <= 0:
        print("Nothing is detected.")
    else:
        print("Both are detected.")


def main():
    cap = cv2.VideoCapture(0)
    time.sleep(3)

    pick_led(cap)

'''
MEMO: 
You can try LED detection with sample images (green and red LED).
Please uncomment the following main function if you want to try it.
'''
# def main():
#     frame = cv2.imread("./img/green_led.jpg", cv2.IMREAD_COLOR)
#     testing_sample_img(frame)


if __name__ == "__main__":
    main()
