[Japanese](./README.md)

# Registrant detection

This is the procedure to detect a registrant by detecting a face from video using OpenCV and verify the detected face matches the one registered in Amazon Rekognition, and sending it to an MQTT Broker.

## Specifications

### Register face

Take a picture of a face with the camera (built-in camera or etc.) using OpenCV and upload it to Amazon Rekognition as a target face.

### Detect face  

Take a picture of a face periodically with the camera using OpenCV. This cycle varies depending on the presence/absence of a face, but it is approximately 1 to 4 seconds.

When detected a face in the picture, verify whether the face is in the registered faces in Amazon Rekognition, and send this event to an MQTT Broker if matched.

The following logs will output in Terminal depending on the detection status:

```sh
$ python3 person_detect.py
not detected. # Face was not detected.  
detected.     # Face was detected.  
matched.      # Face was matched.  
```

## Setup

### Required items

- PC with camera
  - This procedure has been verified with MacBook Pro (2018).

### Procedure

1. Install OpenCV.  
   On MacOS, install it with the following command.  

```sh
$ brew install opencv
```

2. Place the `requirements.txt` file in the same directory as person_detect.py, and install the Python modules needed for the script.  

```
$ pip3 install -r requirements.txt
```

3. Load confidential information into the script as environment variables.    
Copy the `.env.sample` file to create a `.env` file and set the values according to the file contents.

## Register face  

Run `face_register.py` to register a face to Amazon Rekognition.  

```sh
$ python3 face_register.py

# Activate the camera.
```

This script will output the Response data.    
Save ***FaceId*** (included in the response) to the Vantiq Type for master data.

## Detect face  

Run `person_detect.py` to detect a face and send it to an MQTT Broker.  

```sh
$ python3 person_detect.py

# Activate the camera.
```

## Output specifications

| Items         | Details                              |
| ------------ | --------------------------------- |
| Protocol | MQTTS                             |
| Frequency | Transmit once for every new face detects.|
| Format | JSON                              |

```JSON
{
  "camera_id": "string",
  "face_id": "string",
  "timestamp": int,
  "similarity": float
}
```

## Notes
- The sample script can register/detect one face.
- The sample script requires a face photo taken from the front.
- Keep a distance of about 0.5m from the camera.
- The encryption and authentication used in the sample script to communicate with an MQTT broker are simple. You need to modify according to your project's requirements. 
