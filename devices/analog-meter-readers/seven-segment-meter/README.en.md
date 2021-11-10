[Japanese](./README.md)

# 7-segment meter reader

This is the procedure for reading the value of a 7-segment meter and sending it to an MQTT Broker.

## Specifications

### Reading the value of a segment meter

Segment meter reading is accomplished using [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR).  
As for the usage, please refer to the [PaddleOCR Quick Start](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.3/doc/doc_en/quickstart_en.md#22-use-by-code).  

The following demo page shows how `PaddleOCR` detects texts in an image. Please refer to this if necessary:

[https://huggingface.co/spaces/akhaliq/PaddleOCR](https://huggingface.co/spaces/akhaliq/PaddleOCR)

## Setup

### Required items

- 7-segment meter
> The sample script also works with the sample image. You can try it without a meter. The source code for using the sample image has been commented out, so please uncomment it if necessary.

- PC with camera
  - This procedure has been verified with Macbook pro(2018).

>The PaddlePaddle module does not support Arm64 (as of 2021/10/18), so it will not work on Macs equipped with the Apple M1.  

- Full set of this directory  

### Procedure 

1. Install OpenCV.  
   On MacOS, install it with the following command:

```sh
$ brew install opencv
```

2. Place the `requirements.txt` file in the same directory as the segment_meter_reader.py, and install the Python modules needed for the script.  

```
$ pip3 install -r requirements.txt
```

> With Python 3.9.x, the installation of PaddleOCR may fail. In that case, please switch to Python 3.8.x.  


3. Load confidential information into the script as environment variables.    
   Copy the .env.sample file to create a .env file and set the values according to the file contents.  

## Detect the numerical values of the Segment Meter.  

Run `segment_meter_reader.py` to read the values of the Segment Meter and send it to an MQTT Broker.

```sh
$ python3 segment_meter_reader.py
```

## Output specifications

| Items         | Details                  |
| ------------ | --------------------- |
| Protocol   | MQTTS                 |
| Frequency  | Transmit once every 30 seconds|
| Format | JSON                  |

```JSON
{
  "sensor_id": "string",
  "sensing_value": "string",
  "timestamp": int
}
```

## Notes

- Meter value is detected by tuning based on the sample image. The sample script may not detect a meter value correctly if you use an image prepared by yourself. 

- Please check the following notes:
  - Capture so that the meter part occupies most of the camera's field of view.
  - Keep a 0.5 m distance between a meter and a camera.

- The encryption and authentication used in the sample script to communicate with an MQTT broker are simple. You need to modify according to your project's requirements. 
