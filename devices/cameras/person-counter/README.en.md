[Japanese](./README.md)

# Counting the number of persons    

This is the instructions to analyze video captured by a camera with TensorFlow Lite, and when detecting entering an area and leaving an area, send the data to an MQTT Broker.  

## Specifications

### Detect a person

Take a picture with the camera connected to the Raspberry Pi and detect a person. It is developed based on the following sample programs of TensorFlow Lite.  

[TensorFlow Lite Python object detection example with Raspberry Pi](https://github.com/tensorflow/examples/tree/master/lite/examples/object_detection/raspberry_pi)

The models in the above sample programs can detect a variety of objects other than persons. In these instructions, customized to process only when a person is detected.

### Detect entering and leaving a specified area.  

Put a virtual line in the middle of the screen (red dotted line), and regard the left side of the screen as inside the area and regard the right side of the screen as outside the area.  

![](./img/flame0.en.png)

Detect when a person overlaps the virtual line (Figure 1), and then when the person has moved to the left or the right of the virtual line (Figure 2 or 3), publish the event of detection to an MQTT broker.  

Figure 1.  
![](./img/flame1.png)

Figure 2.  
![](./img/flame2.en.png)

Figure 3.  
![](./img/flame3.en.png)

It is confirmed that it can detect when a person walks sideways at a distance of about 1.5 m to 2.0 m from the camera. It may fail to detect when a person is walking too fast due to the high CPU load.  

## Setup  

### Requirements for these instructions.  

- Raspberry Pi  &nbsp; ※ Used Raspberry Pi 3B for this verification.
- [Raspberry Pi Camera Module 2](https://www.raspberrypi.com/products/camera-module-v2/)
- [Raspberry Pi OS with desktop (32bit)](https://www.raspberrypi.org/software/operating-systems/#raspberry-pi-os-32-bit)
- Full set of this directory  


### Instructions

1. Setting up both Raspberry Pi and Raspberry Pi Camera.  
   Connect the Raspberry pi and Raspberry Pi Camera, and start them up.  

2. Insatall "TensorFlow Lite runtime".  
```
$ pip3 install --extra-index-url https://google-coral.github.io/py-repo/ tflite_runtime
```

3. Install the required Python modules and TensorFlow lite models and labels.  
   Place the `requirements.txt` file in the same directory as the `download.sh`, and run the following command.  
```
$ bash download.sh ./tmp
```

4. Load confidential information into the script as environment variables.    
Copy the `.env.sample` file to create a `.env` file and set the values according to the instructions in the file.  

## Detect entering and leaving a specified area.  

Run `person_count.py` and when a person walks in front of the Raspberry Pi Camera, it will send the data to an MQTT Broker depending on the direction.  

```
python3 person_count.py \
  --model ./tmp/detect.tflite \
  --labels ./tmp/coco_labels.txt
```

## Transmission details

| Items         | Details                                                 |
| ------------ | ---------------------------------------------------- |
| Protocol   | MQTTS                                                |
| Frequency     | Event-driven (Transmit when a person crosses the virtual line.) |
| Format | JSON                                                 |

```JSON
{
  "camera_id": "string",
  "timestamp": int,
  "count": int
}
```

## Notes

- Only one person should be caught by the Raspberry Pi's camera.  
- Set up the camera around the same height as a person.  
- A person must walk sideways to the camera.  
- It may fail to detect when walking speed is too fast.  
- This confirmed with a Raspberry Pi 3B, but the usage of some of the CPU cores will be 100%, so prepare a Raspberry Pi with higher specifications depending on the use case.  
- Since the encryption and authentication of the communication path with the MQTT Broker is a brief one, please take measures according to the security level required in the actual project.  
