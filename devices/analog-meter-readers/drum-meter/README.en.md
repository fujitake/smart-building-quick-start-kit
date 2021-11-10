[Japanese](./README.md)

# Drum-type meter reader  

This is the procedure for reading the value of a drum-type meter and sending it to an MQTT Broker.  

## Specifications

### Reading the value of a drum-type meter

Drum-type meter reading is accomplished using [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR).  
As for the usage, please refer to [PaddleOCR Quick Start](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.3/doc/doc_en/quickstart_en.md#22-use-by-code).  

When detected multiple values, the sample script will send the value whose area of the rectangle surrounding the detected value is the largest.  For example, in the following image, the value `02446` in the red frame is sent. 

![](img/readme.jpg)

The following demo page shows how `PaddleOCR` detects texts in an image. Please refer to this if necessary:

[https://huggingface.co/spaces/akhaliq/PaddleOCR](https://huggingface.co/spaces/akhaliq/PaddleOCR)

## Setup

### Required items

- Drum-type meter
> The sample script also works with the sample image. You can try it without a meter. The source code for using the sample image has been commented out, so please uncomment it if necessary.

- PC with camera
  - This procedure has been verified with MacBook Pro (2018).

>The PaddlePaddle module does not support Arm64 (as of 2021/10/18), so it will not work on Macs equipped with the Apple M1.  

- Full set of this directory

### Procedure

1. Install OpenCV.  
   On MacOS, install it with the following command:

```sh
$ brew install opencv
```

2. Place the `requirements.txt` file in the same directory as drum_meter_reader.py, and install the Python modules needed for the script.  

```
$ pip3 install -r requirements.txt
```
> With Python 3.9.x, the installation of PaddleOCR may fail. In that case, please switch to Python 3.8.x.  

3. Load confidential information into the script as environment variables.    
   Copy `.env.sample` file to create `.env` file and set the values according to the file contents.

## Detect the value of drum-type meter

Run `drum_meter_reader.py` to read the value of the drum-type meter and send it to an MQTT Broker.

```sh
$ python3 drum_meter_reader.py
```

## Output specifications 

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

- Meter value is detected by tuning based on the sample image. The sample script may not detect a meter value correctly if you use an image prepared by yourself. 

- Please check the following notes:
  - Capture so that the meter part occupies most of the camera's field of view.
  - Capture the meter part brightly.
  - Capture so that light is not reflected on the meter part.
  - Capture so that the meter part is positioned in front of the camera directly.
  - The sample script is tuned assuming that the meter part is constructed with white text and black background.
  - When the meter part is on rotation, it cannot be read correctly.
- The encryption and authentication used in the sample script to communicate with an MQTT broker are simple. You need to modify according to your project's requirements. 
