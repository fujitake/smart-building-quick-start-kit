[Japanese](./README.md)

# Omron Environment Sensor (2JCIE-BU01)

This is the procedure for acquiring surrounding environment information and sending them to an MQTT broker.  


## Specifications

### Values that can be acquired.

There are two types of Omron Environment Sensors: 2JCIE-BU01 (USB type) and 2JCIE-BL01 (BAG type). There is a slight difference in the values that can be acquired with each, but they can acquire values about the surrounding environment such as Temperature, Humidity, and Barometric pressure. For details, please refer to the manuals.

This procedure uses `2JCIE-BU01(USB type)` which can acquire the value of `eCO2`.  

- [2JCIE-BU01 Environment Sensor (USB Type) User's Manual (pdf)](https://omronfs.omron.com/en_US/ecb/products/pdf/A279-E1-01.pdf)

- [2JCIE-BL01 Environment Sensor User's Manual (pdf)](https://omronfs.omron.com/en_US/ecb/products/pdf/A278-E1.pdf)

## Setup

### Required items

- Omron Environment Sensor (2JCIE-BU01)

- Raspberry Pi 3B+ or 4B
  - [Raspberry Pi OS with desktop (32bit)](https://www.raspberrypi.org/software/operating-systems/#raspberry-pi-os-32-bit)
  - This procedure has been verified with Raspberry Pi 3B+ and 4B. But those are not mandatory.

- Full set of this directory

### Procedure

1. Confirm the MAC address of the Environment Sensor

```
$ sudo hcitool lescan
LE Scan ...
C2:B7:E4:CC:FE:79 Env
※ Env's is the MAC address of the Environment Sensor.
```

2. Place the `envsensor_observer.py` in any directory in the Raspberry Pi
3. Load confidential information into the script as environment variables.
   Copy the `.env.sample` file to create a `.env` file and set the values according to the file contents.  

4. Install the necessary packages and modules

   Place the `requirements.txt` file in the same directory as envsensor_observer.py, and install the Python modules needed for the script. 

```
$ sudo apt install libglib2.0-dev
$ pip3 install -r requirements.txt
```

## Execution

Run `envsensor_observer.py` and confirm that the data is sent

```
$ python3 envsensor_observer.py
Published Event: 2021/09/21 11:03:46
{'pressure': 1005, 'noise': 42, 'temperature': 29, 'env_sensor_id': 'env_sensor1', 'etvoc': 3, 'light': 44, 'eco2': 422, 'humidity': 55}
```

## Output specifications

| Items      | Details               |
| ---------- | --------------------- |
| Protocol   | MQTTS                 |
| Frequency   | once every 10 seconds  |
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
- The encryption and authentication used in the sample script to communicate with an MQTT broker are simple. You need to modify according to your project's requirements. 
