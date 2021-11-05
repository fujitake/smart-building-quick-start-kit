[Japanese](./README.md)

# 7 Segment Meter Reader

This is the instructions for reading the values of a 7 Segment Meter and sending the reading values to an MQTT Broker.



## Specifications

### Reading the values of a Segment Meter

Segment Meter reading is accomplished using [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR).  
As for the usage, refer to [PaddleOCR Quick Start](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.3/doc/doc_en/quickstart_en.md#22-use-by-code).  

The following demo page shows how "PaddleOCR" detects the text in an image. Please refer to it, if necessary.  

[https://huggingface.co/spaces/akhaliq/PaddleOCR](https://huggingface.co/spaces/akhaliq/PaddleOCR)

## Setup

### Requirements for these instructions.

- A 7 Segment Meter to be detected for its values.  
>The script used in these instructions can also work with sample images. The process to use the sample image is commented out, so please uncomment the corresponding part if necessary.  

- PC with camera &nbsp; ※ These instructions use a MacBook Pro (2018) for verification.

>The Paddle module does not support Arm64 (as of 2021/10/18), so it will not work on Macs equipped with the Apple M1.

- Full set of this directory  

### Instructions  

1. Install OpenCV.  
   On MacOS, install it with the following command.

```sh
$ brew install opencv
```

2. Place the requirements.txt file in the same directory as the segment_meter_reader.py, and install the Python modules needed for the application.  

```
$ pip3 install -r requirements.txt
```

> With Python 3.9.x, the installation of PaddleOCR may fail. In that case, please switch to Python 3.8.x.  


3. Load confidential information into the script as environment variables.    
   Copy the .env.sample file to create a .env file and set the values according to the instructions in the file.  

## Detect the numerical values of the Segment Meter.  

Run `segment_meter_reader.py` to read the values of the Segment Meter and send the data to MQTT Broker.

```sh
$ python3 segment_meter_reader.py

```

## Transmission details  

| Items         | Details                  |
| ------------ | --------------------- |
| Protocol   | MQTTS                 |
| Frequency  | Transmit once every 30 seconds30 |
| Format | JSON                  |

```JSON
{
  "sensor_id": "string",
  "sensing_value": "string",
  "timestamp": int
}
```

## Notes

- Confirmed that the detection of the values of the segment meter with based on the sample image. If using the images which are captured by yourself, it may not be possible to detect the values of a Segment Meter correctly. Please prepare them by referring to the following notes.  
  - It is necessary to show only one targeted Meter as a large image to detect the numbers on the meter correctly.
  - Keep a distance of about 0.5 m from the camera.
  - Since the encryption and authentication of the communication path with the MQTT Broker is a brief one, please take measures according to the security level required in the actual project.  
