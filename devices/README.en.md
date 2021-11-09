[Japanese](./README.md)

# Device sample list

Here is the list of device samples. Samples can get value from a device and send it to a broker.
You can experience the data flow from the device to the broker by trying each sample.

***These are just samples for experiencing the flow that gets data from devices to send to brokers. Accuracy and stability are not guaranteed.***

## [Analog meter readers](./analog-meter-readers)

The samples that use a camera to constantly capture images of analog meters such as Drum, LED, Round, and 7-segment meter, and then analyze the images to obtain the values.  

Even if you don't have actual analog meters, sample scripts work with sample images(also included). Each script has been tuned to fit the sample image, so ***it will be required to be re-tuned when used with other images***.  

- [Drum-type meter reader](./analog-meter-readers/drum-meter/README.en.md)
- [LED reader](./analog-meter-readers/led-meter/README.en.md)
- [Round meter reader](./analog-meter-readers/round-meter/README.en.md)
- [7-segment meter reader](./analog-meter-readers/seven-segment-meter/README.en.md)

## [Cameras](./cameras)

The samples that analyze camera images to detect intrusion, count the number of persons, and detect a registrant. 

- [Intrusion detection](./cameras/intrusion-detection/README.en.md)
- [People count](./cameras/person-counter/README.en.md)
- [Registrant detection](./cameras/registrant-detection/README.en.md)

## [Hitachi LG 3D LiDAR Sensor](./hlds-lidar/README.en.md)

The sample uses a Hitachi LG 3D LiDAR sensor to detect the positions of people in an area and to count the number of people entering and leaving the area.


## [Omron Environment Sensor](./omron-env/README.en.md)

The sample uses Omron Environment Sensor to acquire information about the surrounding environment, such as CO2 concentration, temperature, and humidity.    
