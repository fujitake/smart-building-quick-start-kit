[Japanese](./README.md)

# Omron Environment Sensor (2JCIE-BU01)

This is the instructions for acquiring values related to the surrounding environment from Omron Environment Sensor and transmitting them to MQTT Broker.  


## Specifications

### Values that can be acquired.

There are two types of Omron Environment Sensors: 2JCIE-BU01 (USB type) and 2JCIE-BL01 (BAG type). There is a slight difference in the values that can be acquired with each, but they can acquire information about the surrounding environment such as Temperature, Humidity, and Barometric pressure. As for the details, please refer to the User's manual.  

In these instructions, use `2JCIE-BU01(USB type)` which can acquire the value of `eCO2`.  

- [2JCIE-BU01 Environment Sensor (USB Type) User's Manual (pdf)](https://omronfs.omron.com/en_US/ecb/products/pdf/A279-E1-01.pdf)

- [2JCIE-BL01 Environment Sensor User's Manual (pdf)](https://omronfs.omron.com/en_US/ecb/products/pdf/A278-E1.pdf)

## Setup

### Requirements for these instructions.

- Omron Environment Sensor (2JCIE-BU01)  

- Raspberry Pi 3B+ or 4B
  - [Raspberry Pi OS with desktop (32bit)](https://www.raspberrypi.org/software/operating-systems/#raspberry-pi-os-32-bit)
  - Although it is not mandatory to use Raspberry Pi, these instructions use Raspberry Pi 3B+ and 4B for verification.　

- Full set of this directory

### Instructions

1. Confirm the MAC address of the Environment Sensor.  

```
$ sudo hcitool lescan
LE Scan ...
C2:B7:E4:CC:FE:79 Env
※ "Env" is the MAC address of the Environment Sensor.
```

2. Place the `envsensor_observer.py` in any directory in the Raspberry Pi.  
3. Load confidential information into the script as environment variables.    
   Copy the `.env.sample` file to create a `.env` file and set the values according to the instructions in the file.  

4. Install the necessary packages and modules.  
   Place the `requirements.txt` file in the same directory as the envsensor_observer.py, and install the Python modules needed for the application.  

```
$ sudo apt install libglib2.0-dev
$ pip3 install -r requirements.txt
```

## Execution

Run the `envsensor_observer.py` and confirm that the data is sent.    

```
$ python3 envsensor_observer.py
Published Event: 2021/09/21 11:03:46
{'pressure': 1005, 'noise': 42, 'temperature': 29, 'env_sensor_id': 'env_sensor1', 'etvoc': 3, 'light': 44, 'eco2': 422, 'humidity': 55}
```

## Transmission details

| Items      | Details               |
| ---------- | --------------------- |
| Protocol   | MQTTS                 |
| Frequency   | Transmit once every 10 seconds  |
| Format | JSON                  |

**Output sample**
```JSON
{
	"env_sensor_id": "env_sensor1",
	"pressure": 1005,
	"noise": 42,
	"temperature": 29,
	"etvoc": 3,
	"light": 44,
	"eco2": 422,
	"humidity": 55
}
```

## Notes

- Place the Environment Sensor and the Raspberry Pi at a distance within 1 meter.  
- Since the encryption and authentication of the communication path with the MQTT Broker is a brief one, please take measures according to the security level required in the actual project.  
