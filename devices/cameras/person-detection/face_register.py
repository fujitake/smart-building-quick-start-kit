import io
import os
import time

import boto3
import cv2
from dotenv import load_dotenv
from PIL import Image

load_dotenv()

rekognition = boto3.client(
    "rekognition",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("REGION_NAME"),
)

listCollectionsResponse = rekognition.list_collections()

print(f"CollentionId={listCollectionsResponse['CollectionIds']}")
print(f"FaceModelVersions={listCollectionsResponse['FaceModelVersions']}")

collectionId = "person-detection"

if collectionId in listCollectionsResponse["CollectionIds"]:
    response = rekognition.delete_collection(CollectionId=collectionId)

response = rekognition.create_collection(CollectionId=collectionId)


def get_face(cap):
    _, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(frame)
    png = io.BytesIO()
    image.save(png, format="png")
    return png


print("")
print(f"Regist your face.")
print(f"Indexing your face ...")

cap = cv2.VideoCapture(0)
time.sleep(3)

response = rekognition.index_faces(
    CollectionId=collectionId,
    Image={"Bytes": get_face(cap).getvalue()},
    DetectionAttributes=["DEFAULT"],  #'DEFAULT'|'ALL',
    ExternalImageId="test",
    MaxFaces=1,
    QualityFilter="AUTO",  # NONE | AUTO | LOW | MEDIUM | HIGH
)

print(response)
print(f"Indexed {response['FaceRecords'][0]['Face']['FaceId']} .")

print("")
print("Test.")

response = rekognition.search_faces_by_image(
    CollectionId=collectionId,
    Image={"Bytes": get_face(cap).getvalue()},
    MaxFaces=1,
    FaceMatchThreshold=95,
)

print(f"SearchFacesByImageResponse={response}")
