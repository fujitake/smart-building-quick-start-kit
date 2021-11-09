[Japanese](./README.md)

# Detecting registered persons    

Detect a face from the video captured by a camera using OpenCV, and verify whether it matches the face registered in advance using AWS Rekognition. When it matches, it will be sent to an MQTT Broker.

## Specifications

### Register a face

Take a picture of a face with the camera built into the PC using OpenCV. Regard this face photo as the detection target, and upload it to AWS Rekognition.  

To confirm that the upload was done correctly, verify the face with the same photo after the upload. It is successful when the Response is output in Terminal as shown below.

### Detect a face  

Take a picture of a face periodically with the camera built into the PC using OpenCV. The shooting cycle varies depending on the presence or absence of a face, but it is about 1 to 4 seconds.

When a face is in the picture, check the face with AWS Rekognition to verify whether it is the same as the registered face. If they matched, publish to an MQTT Broker.  

Depending on the status of the detection, the following log will be output in Terminal where the program was executed.  

```sh
$ python3 person_detect.py
not detected. # Face was not detected.  
detected.     # Face was detected.  
matched.      # Faces were matched.  
```

## Setup

### Requirements for these instructions.

- PC with camera &nbsp; ※ Used a MacBook Pro (2018) for this verification.  

### Instructions

1. Install OpenCV.  
   On MacOS, install it with the following command.  

```sh
$ brew install opencv
```

2. Place the `requirements.txt` file in the same directory as the sperson_detect.py, and install the Python modules needed for the application.  

```
$ pip3 install -r requirements.txt
```

3. Load confidential information into the script as environment variables.    
Copy the `.env.sample` file to create a `.env` file and set the values according to the instructions in the file.

## Register a face  

Run `face_register.py` to register a face with AWS Rekognition.  

```sh
$ python3 face_register.py

# Activate the camera.
```

This program will output the Response data.    
Set the ***FaceId*** included in the Response to the VANTIQ master data.

## Detect a face  

Run `person_detect.py` to detect a face and send the data to an MQTT Broker.  

```sh
$ python3 person_detect.py

# Activate the camera.
```

## Transmission details

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

- In this sample, only one type of face can be registered and detected.  
- It is necessary to take a picture of the front of the face with a camera.  
- Keep a distance of about 0.5 m from the camera.  
- Since the encryption and authentication of the communication path with the MQTT Broker is a brief one, please take measures according to the security level required in the actual project.  
