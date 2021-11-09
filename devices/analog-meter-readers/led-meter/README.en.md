[Japanese](./README.md)

# LED reader

This is the instructions for reading the color of the LED lamp and sending the reading value to an MQTT Broker.  

## Specifications  

### Reading the values of a LED.

The lighting status of the LED is accomplished by image processing using OpenCV. It is tuned to read Green (OpenCV Color Space Hue 65-70) or Red (OpenCV Color Space Hue 175-180), and considers it as "Lighting" when this color is detected in the image.  

At this point, it is only judging ***"whether or not there is green or red in the image"***, so it is necessary to show only one targeted LED as a large image to make it work properly.

## Setup

### Requirements for these instructions.

- LED lamp to be detected.
> The script used in these instructions can also work with sample images. The process to use the sample image is commented out, so please uncomment the corresponding part if necessary.  

- PC with camera &nbsp; ※ These instructions use a MacBook Pro (2018) for verification.

- Full set of this directory

### Instructions

1. Install OpenCV.  
   On MacOS, install it with the following command.  

```sh
$ brew install opencv
```

2. Place the `requirements.txt` file in the same directory as the led_status_observer.py, and install the Python modules needed for the application.  

```
$ pip3 install -r requirements.txt
```

3. Load confidential information into the script as environment variables.    
   Copy the ``.env.sample`` file to create a ``.env file`` and set the values according to the instructions in the file.

## Detect Green LED or Red LED.   

Run `led_status_observer.py` to detect Green LED or Red LED and send the data to an MQTT Broker.  

```sh
$ python3 led_status_observer.py

```

## Transmission details

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

- It is necessary to show only one targeted LED as a large image to detect the LED lighting correctly.  
- Since "Lighting" is judged based on "whether the color is present" in the image, it is necessary to change the logic for judging "Lighting" when the number of LEDs increases to two.  
- It is assumed that there are no LEDs of any color other than Green or Red. Since "Lighting" is judged based on whether the color is present in the image, the presence of LEDs other than Green or Red may cause misjudge that the LED is "Lighting".  
- It is recommended to use a camera from the same manufacturer. The colors of the images captured will vary depending on the camera.
- Since the encryption and authentication of the communication path with the MQTT Broker is a brief one, please take measures according to the security level required in the actual project.  
