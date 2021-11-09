[Japanese](./README.md)

# List of Device Samples

Here is the list of device samples. In each sample, it is possible to get values from the devices and send them to an broker. Please try it and grasp the flow.  

***This is just a sample to experience how the data is acquired from the device and sent to an broker, and the accuracy is not guaranteed.***

## [Analog meter readers](./analog-meter-readers)

The samples that use a camera to constantly capture images of analog meters such as Drum, LED, Round, and 7-segment meter, and then analyze the images to obtain the values.  

Even if don't have an actual analog meter, it is possible to check the behavior with sample images. Each script has been tuned to fit the sample image, so ***it will be required to be re-tuned when used with other images***.  

- [Drum type meter reader](./analog-meter-readers/drum-meter)
- [LED reader](./analog-meter-readers/led-meter)
- [Round meter reader](./analog-meter-readers/round-meter)
- [7 segment meter reader](./analog-meter-readers/seven-segment-meter)

## [Cameras](./cameras)

The samples that analyze camera images to detect intrusion, to count the number of persons, and to detect registered persons.  

- [Intrusion detection](./cameras/intrusion-detection)
- [People count](./cameras/person-counter)
- [Registrant detection](./cameras/registrant-detection)

## [Hitachi LG 3D LiDAR Sensor](./hlds-lidar)

The sample uses Hitachi LG 3D LiDAR sensor to detect the location of people in an area and to count the number of persons entering and leaving the area.  


## [Omron Environment Sensor](./omron-env)

The sample uses Omron Environment Sensor to acquire information about the surrounding environment, such as CO2 concentration, temperature, and humidity.    
