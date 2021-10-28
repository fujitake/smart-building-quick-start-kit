import datetime
import io
import json
import os
import time

import boto3
import cv2
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
from PIL import Image

load_dotenv()

collectionId = "person-detection"
rekognition = boto3.client(
    "rekognition",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("REGION_NAME"),
)


def init_rekognition():
    listCollectionsResponse = rekognition.list_collections()

    print(f"CollentionId={listCollectionsResponse['CollectionIds']}")
    print(f"FaceModelVersions={listCollectionsResponse['FaceModelVersions']}")

    if not (collectionId in listCollectionsResponse["CollectionIds"]):
        rekognition.create_collection(CollectionId=collectionId)


def save_frame_camera(cap):
    _, frame = cap.read()
    return frame


def detect_faces(frame):
    image_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    facerect = cv2.CascadeClassifier(
        "./models/haarcascade_frontalface_default.xml"
    ).detectMultiScale(image_gray, scaleFactor=1.1, minNeighbors=2, minSize=(30, 30))
    if len(facerect) > 0:
        print("detected.")
        return True
    else:
        print("not detected.")
        return False


def match_faces(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    image = Image.fromarray(frame)
    png = io.BytesIO()
    image.save(png, format="png")

    try:
        response = rekognition.search_faces_by_image(
            CollectionId=collectionId,
            Image={"Bytes": png.getvalue()},
            MaxFaces=1,
            FaceMatchThreshold=95,
        )
        if response["FaceMatches"]:
            print("matched.")
            similarity = response["FaceMatches"][0]["Similarity"]
            face_id = response["FaceMatches"][0]["Face"]["FaceId"]
            return face_id, similarity
        else:
            print("not matched.")
            return None, None
    except:
        print("failed face matches.")
        return None, None


def post_face_id(face_id, similarity):
    body = json.dumps(
        {
            "camera_id": "registrantcamera_1",
            "face_id": face_id,
            "timestamp": int(time.mktime(datetime.datetime.now().timetuple())),
            "similarity": similarity,
        }
    )

    client = mqtt.Client()
    client.username_pw_set(os.getenv("MQTT_USER"), password=os.getenv("MQTT_PASSWORD"))
    client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLSv1_2, ciphers=None)
    client.tls_insecure_set(True)
    client.connect(os.getenv("MQTT_BROKER_HOST"), 8883)
    client.publish(os.getenv("MQTT_TOPIC"), body)
    client.disconnect()


cap = cv2.VideoCapture(0)
last_result = False

while True:
    frame = save_frame_camera(cap)

    # Did you detect a face?
    if not detect_faces(frame):
        # If not detected
        last_result = False
        continue

    # Did you get a face match?
    face_id, similarity = match_faces(frame)
    if not face_id:
        # If there is no match
        last_result = False
        continue

    # Was there a match last time?
    if last_result:
        # If there was a match last time
        continue

    # Send results
    post_face_id(face_id, similarity)
    last_result = True

    time.sleep(1)
