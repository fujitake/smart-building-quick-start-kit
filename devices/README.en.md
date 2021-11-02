[Japanese](./README.md)

# List of Device Samples

Here is the list of device samples. In each sample, it is possible to get values from the devices and send them to the broker. Please try it and grasp the flow.  

***This is just a sample to experience how the data is acquired from the device and sent to the broker, and the accuracy is not guaranteed.***

## [Analog meter readers](./analog-meter-readers)

The samples that use a camera to constantly capture images of analog meters such as Drum, LED, Round, and 7-segment meters, and then analyze the images to obtain the values.  

Even if don't have an actual analog meter, it is possible to check the behavior with sample images. Each script has been tuned to fit the sample image, so ***it will be required to be re-tuned when used with other images***.  

## [Cameras](./cameras)

The samples that analyze camera images to detect intrusion, count the number of persons, and detect registered persons.  

## [Hitachi LG 3D LiDAR Sensor](./hlds-lidar)

The sample that detects the location of persons in an area and counts their entry/exit into/out of an area, using Hitachi LG 3D LiDAR sensor.  

## [Omron Environment Sensor](./omron-env)

The sample that acquires information about the surrounding environment, such as CO2 concentration, temperature, and humidity, using Omron Environment Sensor.  
