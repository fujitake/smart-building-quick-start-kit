[Japanese](./README.md)

# Analog Round Meter Reader

## Overview and Prerequisite

This is the instructions for for reading the values of a round shaped analog meter and sending the reading values to an MQTT broker.  

For high accuracy in reading values, it is necessary for the camera to have a large image with only a Round Meter in focus and as few shadows as possible.

It is not suitable for high accuracy requirements, as this was created for the purpose of experiencing the process of Smart Building.

## Requirements for these instructions.
- An Analog Round Meter
    - There should be only one needle and no multiple graduations.　　
    - [Reference image](#meter-image)
>As a stand-alone script behavior, the detection target is not limited to thermometer. In this **Smart Building Quick Start Kit**, it is used as reading a thermometer.   

- Python script
    - analog_round_meter_reader.py

> The script used in these instructions can also work with sample image. So, it is possible to execute this even without a Round meter and/or Raspberry pi. The process to use the sample image is commented out, so please uncomment the corresponding part if necessary.

- PC with a camera  
    - These instructions use Raspberry pi 4B + Picamera v2 for verification.
- An MQTT Broker


## Instructions


1. Configure the environment variables used in the script.  

Create an `.env` file in the same directory as the script and configure the information about your MQTT Broker, the minimum and maximum values of the graduations of the Analog Round Meter, and the minimum and maximum values of the angles of the Analog Round Meter.  

```.env
# Mqtt broker
MQTT_HOST = 'your-broker.com'
MQTT_PORT = 8883
MQTT_TOPIC = '/analog_meter/temperature'
MQTT_USER = "your-username"
MQTT_PASSWORD = 'your-password'

# Analog round meter
MIN_ANGLE = 80
MAX_ANGLE = 280
MIN_VALUE = -30
MAX_VALUE = 60
```
>**How to set up the Analog Round Meter**

<a id="meter-image"></a>

【Reference image】

<img src="./img/calibration.jpg" width="400">

For the reference image, the configuration information is the followings.  

```
MIN_ANGLE = 80  # Minimum value of angle
MAX_ANGLE = 278 # Maximum value of angle
MIN_VALUE = -25 # Minimum value of graduations
MAX_VALUE = 55  # Maximum value of graduations
```
>Run the script, then the angle will be displayed around the meter as shown in the Reference image. Once running the script with an arbitrary value on a trial basis and grasping the angle, it is easy to configure.


2.  Run `analog_round_meter_reader.py`.  
>Check the script before running it, and if there are any modules that are not installed in your environment, install the necessary ones.  
```
$ python analog_round_meter_reader.py
```


**Transmission details**

|Items|Details|
|---|---|
|Protocol|MQTTS|
|Frequency|Transmit once every 60 seconds|
|Format|JSON |

```JSON
{
   "deviceId": "temp_meter_001",  # the ID of Device
   "temperature": 27.48 # Temperature (℃)
}
```
