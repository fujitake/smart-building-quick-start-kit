[Japanese](./README.md)

# LED reader

This is the instructions for reading the color of the LED lamp and sending it to an MQTT Broker.  

## Specifications  

### Reading the value of a LED

LED reading is accomplished using OpenCV. It is tuned to read Green (OpenCV Color Space Hue 65-70) or Red (OpenCV Color Space Hue 175-180) and considers it as "Lighting" when these colors are detected in the image. 

At this point, it is only judging ***"whether or not there is green or red in the image"***, so it is necessary to show only one targeted LED as a large image to make it work properly.

## Setup

### Requirements for these instructions.

- LED lamp
> The sample script also works with the sample image. The source code for using the sample image has been commented out, so please uncomment it if necessary.

- PC with camera &nbsp; ※ verified with Macbook pro(2018)

- Full set of this directory

### Instructions

1. Install OpenCV.  
   On MacOS, install it with the following command:

```sh
$ brew install opencv
```

2. Place the `requirements.txt` file in the same directory as the led_status_observer.py, and install the Python modules needed for the script.  

```
$ pip3 install -r requirements.txt
```

3. Load confidential information into the script as environment variables.    
   Copy the `.env.sample` file to create a `.env file` and set the values according to the instructions in the file.

## Detect Green LED or Red LED.   

Run `led_status_observer.py` to detect Green LED or Red LED and send it to an MQTT Broker.  

```sh
$ python3 led_status_observer.py

```

## Output specifications 

| Items         | Details                  |
| ------------ | --------------------- |
| Protocol   | MQTTS                 |
| Frequency  | Transmit once every 30 seconds  |
| Format | JSON                  |

```JSON
{
  "sensor_id": "string",
  "sensing_value": "string",
  "timestamp": int
}
```

## Notes

- Capture so that one LED lamp occupies most of the camera view.
- The sample script does not work if two or more LED lamps are detected.
- Only read and green can be detected.
- Colors of images vary slightly depending on the type of camera.
- The encryption and authentication used in the sample script to communicate with an MQTT broker are simple. You need to modify according to your project's requirements. 
