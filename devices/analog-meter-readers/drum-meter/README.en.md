[Japanese](./README.md)

# Drum Type Meter reader  

This is the instructions for reading the values of a Drum Type Meter and sending the reading values to an MQTT broker.  

## Specifications

### Reading the values of a Drum Type Meter

Drum Type Meter reading is accomplished using [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR).  
As for the usage, refer to [PaddleOCR Quick Start](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.3/doc/doc_en/quickstart_en.md#22-use-by-code).  

When a Drum Type Meter is read and multiple values are detected, calculate the area of the rectangle (Bounding Box) surrounding the detected values, and send the value whose area is the largest. For example, in the sample image which is in the directory, the value `02446` in the red frame will be sent.  

![](img/readme.jpg)

The following demo page shows how "PaddleOCR" detects the text in an image. Please refer to it, if necessary.  

[https://huggingface.co/spaces/akhaliq/PaddleOCR](https://huggingface.co/spaces/akhaliq/PaddleOCR)

## Setup

### Requirements for this instruction.

- Drum Type Meter to be detected.  
> The script used in this instructions can also work with sample images. The process to use the sample image is commented out, so please uncomment the corresponding part if necessary.  

- PC with camera &nbsp; ※ This instructions uses a MacBook Pro (2018) for verification.

>The Paddle module does not support Arm64 (as of 2021/10/18), so it will not work on Macs equipped with the Apple M1.  

- Full set of this directory

### Instructions

1. Install OpenCV.  
   On MacOS, install it with the following command.  

```sh
$ brew install opencv
```

2. Place the `requirements.txt` file in the same directory as the drum_meter_reader.py, and install the Python modules needed for the application.  

```
$ pip3 install -r requirements.txt
```
> With Python 3.9.x, the installation of PaddleOCR may fail. In that case, please switch to Python 3.8.x.  

3. Load confidential information into the script as environment variables.    
   Copy the .env.sample file to create a .env file and set the values according to the instructions in the file.  

## Detect the numerical value of the Drum Type Meter.  

Run `drum_meter_reader.py` to read the sample image of the Drum Type Meter which is in directory and send the data to VANTIQ.  

```sh
$ python3 drum_meter_reader.py
```

## Transmission details  

| Items        | Details                  |
| ------------ | --------------------- |
| Protocol   | MQTTS                 |
| Frequency  | Transmit once every 30 seconds |
| Format | JSON                  |

```JSON
{
  "sensorId": "string",
  "sensing_value": "string",
  "timestamp": int
}
```

## Notes

- This instruction detects the numerical values by making adjustments based on the sample images. If using the images which are captured by yourself, it may not be possible to detect the values correctly. Please prepare them by referring to the following notes.
  - Capture a large, bright image of the meter only.  
  - Make sure that the reflection of light does not appear on the meter.  
  - Take a picture with the meter part directly in front of you.  
  - It is adjusted assuming that the meter part is white text on a black background.  
  - When a number is currently on rotation, it cannot be read correctly.  
- Since the encryption and authentication of the communication path with the MQTT Broker is a brief one, please take measures according to the security level required in the actual project.  
