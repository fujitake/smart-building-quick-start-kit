[Japanese](../ja/details.md)

# Smart Building Quick Start Details

## Table Of Contents  

1. [Introduction](#at-first)
2. [Device Layer](#device-layer)

    2.1. [Specifications of the device](#device-spec)

    2.1.1. [What the device can do?](#what-device-can-do)

    2.1.2. [Quality of the device](#device-quality)

    2.1.3. [How to transmit the data](#device-data-transmission)

    2.1.4. [How to supply the power](#device-power-supply)

    2.1.5. [Requirements for installation](#device-installation)

    2.1.6. [Specifications of the data](#device-data-spec)

    2.2. [Price](#device-price)

    2.3. [Laws and Regulations](#device-laws)

    2.4. [Data loss](#device-data-loss)

    2.5. [Path of transmitting data to the Data Integration Layer (Vantiq)](#device-data-path)

    2.6. [Operation in the case of anomaly or malfunction](#device-operation)

    2.7. [Summary of Device Layer](#device-summary)

3. [Data Integration Layer](#data-integration-layer)

    3.1. [Master data Management](#data-integration-master-data)

    3.2. [Data Store](#data-integration-data-store)

    3.3. [Vantiq](#data-integration-vantiq)

    3.3.1. [Frequently used Activity Patterns](#data-integration-activity)

    3.3.2. [Performance-conscious Implementation](#data-integration-performance)

    3.3.2.1. [Lighten the processing per task](#data-integration-lighten)

    3.3.2.2. [Reduce and Distribute the number of query issuances.](#data-integration-reduce-queries)

    3.3.2.3. [Reduce the number of concurrent executions](#data-integration-reduce-simultaneous)

    3.3.2.4. [Confirm that it actually provides performance.](#data-integration-performacne-test)

    3.4. [Summary of Data Integration Layer](#data-integration-summary)

4. [Data Providing Layer](#data-providing-layer)

    4.1. [PULL type (API) data providing](#data-providing-pull)

    4.2. [PUSH type (Broker) data providing](#data-providing-push)

    4.3. [Summary of Data Providing Layer](#data-providing-summary)

<br />
<br />

<a id="at-first"></a>
## 1. Introduction

This repository summarizes the details of the knowledge, concepts, and precautions necessary for Smart Building with Vantiq. Smart Building includes a wide range of elements, from devices to clouds, and only a few people are able to grasp the whole picture. But ultimately what we need to think about is just the simple flow of how to collect, transform, and provide the data. It would be appreciated if you would read this document with an awareness of how this process can be achieved.  

This content is only the basic form, so there are areas that need to be changed as necessary for each requirement, but the basic idea remains the same.  

This document is also organized according to the layers of the following figure.  

<img src="../img/layers.en.png" width="1000">

<a id="device-layer"></a>
## 2. Device Layer

Devices are the most important element of all IoT projects, regardless of Smart Building. No matter what the plan is, it is impossible to accomplish it without a device that can acquire the data to make it possible. Also, the accuracy of the device is directly related to the accuracy of the data of the entire system. In other words, making a mistake in device selection will directly lead to the failure of the project itself, so it is necessary to select them carefully.  
Now move to the points to be checked for selecting the devices.  


<a id="device-spec"></a>
### 2.1. Specifications of the device

It is necessary to check the specifications in detail to see whether they can accomplish what you want to achieve. If the device is not suitable, the project will fail as it is and time and money will be wasted, so this phase should be done carefully even if it takes a long time.  

<a id="what-device-can-do"></a>
### 2.1.1. What the device can do?

First of all, as a matter of course, it is necessary to know exactly what the device is capable of. For example, when speaking of a "temperature sensor," it is necessary to confirm &nbsp;① what range of temperature it can measure (detection range), &nbsp;② what units it can measure (resolution), and &nbsp;③ how much the allowable margin of error it have (precision). As an example, suppose you want to provide an alert function when the temperature exceeds 100°C. If selecting a temperature sensor whose detection range is -30°C to +60°C, it is obviously not possible to achieve this function. It's not just a "temperature sensor," but first it is necessary to understand what the device can do with such clarity that it is a "temperature sensor that can cover a range of -30 to 60°C in 0.1°C increments with he allowable margin of error of about ±0.2°C". It is also important to confirm that the coverage area that can be covered by each device, in the case of using AI cameras or other devices that keep looking at a particular area.  


<a id="device-quality"></a>
### 2.1.2. Quality of the device

Frequent device failures, poor fire resistance and water resistance, etc. can cause unexpected maintenance costs and accidents. It is basic, but it should be confirmed for quality. It is also as a meaning of actually checking the accuracy, it is safe to purchase and verify the product before deciding to adopt it.  

<a id="device-data-transmission"></a>
### 2.1.3. How to transmit the data

Confirm that how to transmit the the sensed contents to other layers. For example, using a temperature sensor, it does not make sense to have only a module with a sensor element. It is only possible to transmit the sensed contents to other layers when used in conjunction with a microcontroller or an IoT gateway. It is necessary to confirm because it depends on the device, such as one that plugs into an IoT gateway or has a BLE connection, or one that is integrated as a service and can transmit the data directly to the cloud. Also confirm that the path after an IoT gateway (e.g., is it WiFi, LTE communication using a SIM, etc.).

<a id="device-power-supply"></a>
### 2.1.4. How to supply the power

Whether a device is battery-powered or not greatly affects the location of installation and ease of maintenance. In the case of Smart Building, battery-powered devices are less likely to be candidates, but it is safer to confirm.

<a id="device-installation"></a>
### 2.1.5. Requirements for installation

There are two installation requirements. The first is the device installation requirement. It means, in what kind of environment and under what kind of conditions it is installed, it can provide the performance defined in the specifications. If the device is not installed correctly, it will not perform to the specifications, so once understanding "what the device can do", confirm "the way to use it to accomplish its performance".
For example, even if there is an AI camera that can detect a person's face with 100% precision, it may not be able to detect a person's face at all if the camera is installed in a place where the image is blown out highlights or in a dark place.
The second is the installation requirements requested from building owner. There are not many cases where devices can be installed anywhere in the building as you like. Considering the landscape and the replacement due to malfunction, it should be installed in a location approved by the building owner.  

It is important to consider the following: "With this device, it is possible to do what we want to do. But can this device be installed in this building in a way which maintains easy?"


<a id="device-data-spec"></a>
### 2.1.6. Specifications of the data

Confirm the protocol, the format, the size, and the frequency of transmission.The protocol and the format determines how the data can be linked to other layers. The size and the frequency of transmissions have a great deal to do with the performance of the opposing system and its implementation.  

<a id="device-price"></a>
### 2.2. Price

Calculate the price and the number of devices, IoT gateways, WiFi routers, SIM cards, and other necessary items and confirm whether the cost is worth it. Some devices may be routed through a dedicated cloud service, and the pricing model may include that as well.  

<a id="device-laws"></a>
### 2.3. Laws and Regulations

Be especially careful when dealing with devices from overseas.Check whether the device meets (or is able to meet) the laws and regulations for the device, such as whether it has obtained the Technical Compliance Mark and/or PSE Mark, as well as the laws and regulations imposed on the business (such as the Personal Information Protection Law). The device should be in compliance with Japanese law. Also, be careful when handling data that contains personal information.

<a id="device-data-loss"></a>
### 2.4. Data loss

Especially in the case of wireless connections, data loss will occur, so it is necessary to consider increasing the number of devices to reduce the loss rate, supplementing the data on the application side, and designing the system so that it will not be affected by the loss.  

<a id="device-data-path"></a>
### 2.5. Path of transmitting data to the Data Integration Layer (Vantiq)

It is necessary to consider the path how the data will be transmitted from the device to Vantiq, the Data Integration Layer. There are two main patterns for providing the data to Vantiq. The first is to use Vantiq's REST API. The second is via a broker with protocols such as MQTT and Kafka.  

First of all, when using Vantiq's REST API, it should be necessary to set the Access Token issued by Vantiq in the Header and then make an HTTP request. If the device has this feature, it is possible to use this method. There are some cases where HTTP requests can be made but the settings of the Header cannot be configured, in that case  case there are other options such as using AWS Lambda or Azure Functions as a relay.  

Using the REST API is simple, but has the following disadvantages.  
① The management of Access Tokens becomes complicated.  
Since the Access Token is embedded in the device, when it needs to be updated due to expiration or leakage of the token, it is necessary to replace the token on all devices, depending on how the token was distributed.  
② Impact on the performance of Vantiq.  
Since HTTP is not a lightweight as a protocol, it will consume a lot of Vantiq resources if the number of devices is large.    

Secondly, the method via a broker eliminates the need to issue an Access Token to the device (Authentication Information to the broker are still required). It can also use MQTT, AMQP, and Kafka protocols, which are lightweight compared to HTTP.  
The disadvantages are the followings.  
① Need to prepare a broker.  
For example, it is required to prepare AWS AmazonMQ and/or Azure Event Hubs. The characteristics of each broker, such as performance and required settings, should be understood.    
② Difficulty of protocol support is higher than HTTP.
There is no problem on the Vantiq side because MQTT, AMQP, and Kafka clients are prepared in advance, but not many devices support MQTT, AMQP, and Kafka even if they support HTTP.    

To summarize, it is easier to operate via a broker unless the number of devices is extremely small. It is required to build a broker, but it can be used a fully managed one. Also, managing devices with AWS IoT Core, Azure IoT hub, etc. makes it easy to support protocols, as data from devices can be routed to the broker when it is received.  

**One word about Device Management Service**
>There are services that often advertise device management, but what is a device in this context? It is never called "Sensor Management", in my opinion. These services can manage devices that are connected to the Internet, so to be precise, it would be "IoT gateway management".  Even if it can manage the IoT gateway, it cannot manage the sensors connected to it (of course, this is not a problem if the sensing part and the IoT gateway functions are integrated). It is better to understand what exactly the service can do before deciding to implement it.  

<a id="device-operation"></a>
### 2.6. Operation in the case of anomaly or malfunction

Since there is no machine that will never break down, any device will surely anomaly or malfunction at some point. It is necessary to have a system design and organizational operation mechanism in order to identify devices that are experiencing anomalies and to ensure that there are no problems when replacements occur.  

<a id="device-summary"></a>
### 2.7. Summary of Device Layer

As this is the most important layer, there are many things to confirm. To summarize simply, the following should be confirmed.   
① It is possible to get the data to accomplish the plan.  
② It is possible to establish a route to transmit the acquired data to Vantiq.  
③ It should be in a state to be able to operate continuously.

<a id="data-integration-layer"></a>
## 3. Data Integration Layer

The Data Integration Layer is the layer that creates the data to be ultimately provided to users. It performs data integration processes such as combining data from multiple sensors, assigning Master data to sensor data, threshold judgment, and transformation. Vantiq is responsible for directly processing data from the Device Layer, while the Master data required for that processing is managed by other applications such as those separate from Vantiq. Also, because Vantiq specializes in stream processing, it retains the most recently created data, but does not retain older data, so if it is necessary to save the processed data for analysis, etc., it should be saved in a separate data store.

<a id="data-integration-master-data"></a>
### 3.1. Master data Management

The data sent from the device is not used as it is, but by combining the necessary contents as Master data in addition to the data sent, such as the device name that is easy for persons to understand, its installation location and coordinates, etc., and finally the data to be provided to users can be created.
例For example, to achieve the use case that " Notify when the temperature in a room exceeds 35 °C," it is required to have information about which room the sensor is installed in, in addition to the temperature data. If the data sent from the device measuring the temperature originally contains the installation location, nothing needs to be done, but in some cases it contains only minimal data (e.g. serial number and temperature data).  

In such a case, holding the Master data in advance in Vantiq and combining it with the data sent from the device will provide the necessary information for the subsequent processing.
In a Smart Building, a wide variety of devices are used, and each of the data contents is completely different. It is possible to respond to various use cases by being ready to provide all the necessary information in Vantiq side.  

What is needed is the role of managing the Master data. Since Vantiq is the one that actually uses the Master data, it is technically possible to manage the Master data directly in Vantiq, but it is preferable to separate them from the point of view of responsibility boundary point.  

Since Vantiq will hold the Master data in Type, the application which takes on this role needs to be able to CRUD operations for the records of Vantiq's Type using the REST API, while having the Master data in its own DB.  

<a id="data-integration-data-store"></a>
### 3.2. Data Store  

This is the data store for storing the data processed by Vantiq and which needs to be stored for a long time. Continuously store the following data according to the requirements.  
- Data provided to users created by Vantiq  
- Raw data sent from devices  
- Log data  
Since the data to be stored will continue to increase from the start of the system's operation, the cost will increase. Instead of storing everything, build and configure the system so that it stores the minimum amount of data required.  

It is required to be able to receive data from Vantiq. Since the performance of Vantiq is often higher than that of an ordinary DB, it is not recommended to execute APIs directly on Vantiq to receive data. It is better to implement it via a broker or a queue to keep it more loosely coupled.  


<a id="data-integration-vantiq"></a>
### 3.3. Vantiq

This is the core of the Data Integration Layer. This section describes frequently used Activity Patterns and cautions for implementation.  

<a id="data-integration-activity"></a>
### 3.3.1. Frequently used Activity Patterns

Vantiq provides a variety of Activity Patterns, and introduce some of the most frequently used and essential ones.  

- Transformation
    - Used to perform the data transformation such as deleting unnecessary parameters, renaming parameters, and adjusting data units. The data sent from the device is in a different format for each device, so this Activity absorbs the differences between devices and converts the data into the format to be provided to users finally.  

- Enrich
    - Since the contents of the records of Type can be added to the data to be stream processed, it is often used to add Master data to the data sent from the device. As the parameter with the same name must exist in the Type as the data to be processed, it is often done with Procedure together with Transformation.  

- Filter
    - This function passes only the data that meets the specified conditions to the next process. This function is used for threshold judgment and conditional branching.  

- SaveToType  
    - It is used to save the data in Type. There is an `Upsert` option, which is used to keep in Vantiq only the most recent one for each device.

- Procedure
    - This is the most versatile Activity because it is possible to call your own Procedures. It is used everywhere, and the most common case is to create your own process to send data from Vantiq to other systems, and then call the Procedure. It is also use ***PublishToSource*** when sending the data to other systems, but it is often used Procedure because it does not allow detailed settings such as error handling.  


<a id="data-integration-performance"></a>
### 3.3.2. Performance-conscious Implementation  

Vantiq can provide a high performance platform, but it may not be able to provide the performance depending on how it is implemented. It requires to understand the characteristics of Vantiq and to implement it accordingly. Especially, be more careful for those who are used to implementing web applications. Vantiq has the elements such as web (or mobile) client, DB, and application, so it is possible to implement 3-tier architecture for a traditional  web applications.
However, it is a service that specializes in stream processing, so applying in the common sense of web application development as is will result in failure.
It should be considered as an asynchronous and parallel processing of small processes at high speed.  

<a id="data-integration-lighten"></a>
### 3.3.2.1. Lighten the processing per task

When implementing an application, it is necessary to lighten the content to be processed per task. When using Procedure, any number of processes can be grouped together and called in a single task. However, since Vantiq performs load balancing in units of one task, performance will be improved by dividing it into multiple tasks rather than executing heavy processing in one task. Typical heavy processing is that which needs to wait for the response of a system other than Vantiq, such as issuing SQL that cannot be completed in memory alone, or executing an external API.  

<a id="data-integration-reduce-queries"></a>
### 3.3.2.2. Reduce and Distribute the number of query issuances.

When referring to the Master data stored in Type, or writing data to it, queries will be issued. This process is heavier than a process that is completed within memory only. Therefore, it is important to reduce the number of query issuances and distribute queries if better performance is to be expected.  

For example, according to the requirements, it may necessary to add multiple types of Master data to the data transmitted from a single device. In that case, it can be implemented in Procedure as the following.  

```
PROCEDURE attachMasterData(event)
event.master1 = SELECT ONE FROM master1 WHERE device_id == event.deviceId
event.master2 = SELECT ONE FROM master2 WHERE device_id == event.deviceId
event.master3 = SELECT ONE FROM master3 WHERE device_id == event.deviceId
return event
```

The query is issued three times in one Procedure. When calling this Procedure in an application task, the query will be issued three times in one task. It is easy for maintenance and refurbishment, but this will not provide performance (in other words, if the performance is not important, this method is preferable). The followings are two methods to handle this.  

① Divide into 3 Procedures, 3 Tasks.  
This one is simple method. If the performance is not good because it is grouped together, then it is better to divide the queries. Even this alone will improve the performance. However, the number of query issuances itself has not been reduced.  

② Prepare a Type for denormalized Master data.  
This is a method to create Type which groups the necessary Master data in advance in order to issue a query only once. In consideration of the Master data management application that updates Vantiq Master data, it is possible to use the following methods. &nbsp;① Have the Type which groups the Master data updated directly. &nbsp;② In the case that Vantiq has a Type that is a DB and a replica of the Master data management application, prepare a Vantiq application or Rule that works as a trigger when those Types are updated, and update the Type that groups the Master data.  
This is recommended because it minimizes the number of query issuances and simplifies the implementation.
Please consider this method while keeping a balance with maintainability.  


<a id="data-integration-reduce-simultaneous"></a>
### 3.3.2.3. Reduce the number of concurrent executions

Trying to process a large amount of data all at once with less than a 0.1 second latency, it will consume a lot of resources at once. Therefore, the process needs to be shifted as slightly as possible. Vantiq has ***Scheduled Event***, but when using it to issue a large number of queries at the exact same time, the entire cluster will be overloaded.  

<a id="data-integration-performacne-test"></a>
### 3.3.2.4. Confirm that it actually provides performance.

It is necessary to confirm that sufficient performance can be provided under the actual load of production operation. As it is not feasible to actually use real sensors and IoT gateways for performance testing, a performance testing tool is used to confirm the results.  

<a id="data-integration-summary"></a>
### 3.4. Summary of Data Integration Layer

In order to implement the Data Integration Layer, it is important to understand Vantiq which is as core. It requires a different way of thinking than a web application implementation, and depending on the required performance, it may sacrifice some maintainability.
However, there is no need to think too hard about it, just design and implement it with the following points in mind.  
- Make each processing unit small.  
- Minimize the frequency of Type (DB) usage.  
- Don't overload at once at the same timing.  


<a id="data-providing-layer"></a>
## 4. Data Providing Layer

This is the layer that provides the data for users to be able to use it finally. By having this layer, users do not need to be aware of the lower layers. Data is provided in two main styles: PULL type and PUSH type. Consider the method of providing the data depending on the characteristics and the type of data to be provided.  

For example, if the data to be provided is only the most recent one sent by the device, it is convenient for Vantiq, the Data Integration layer, to keep the entity of the data to be provided in Type. There is also the possibility of providing data from sources other than Vantiq when considering Smart Building as a whole. For these reasons, hide the elements in the Data Integration Layer with this layer.　In this case, the data can be acquired by providing users with a REST API endpoint of the Type of Vantiq and an Access Token. However, distributing an Access Token of Vantiq to users is not preferred as it would be unmanageable, and as for the domain, being the domain of Vantiq is not always preferred to users.  

Users can use APIs and brokers whose interfaces are commonized, regardless of what elements are there, without being aware of from the Device Layer to the Data Integration Layer.  


<a id="data-providing-pull"></a>
### 4.1. PULL type (API) data providing  

If the data to be provided is limited, such as only the most recent of sensing result, the data may be stored in Type of Vantiq, and it may also be provided via REST API. However, it does not have users execute the REST APIT of Vantiq directly, but provides data via AWS API Gateway/Lambda or Azure API Management/Functions.

Users execute APIs provided by AWS API Gateway or Azure API Management, and Lambda or Functions, which is entity of each, executes the REST API of Vantiq to acquire the data.  

In the case of allowing to provide old data as well, store the data processed by Vantiq in another data store via a broker, and provide the data via the API as above. Lambda and Functions will manage that data store.  


<a id="data-providing-push"></a>
### 4.2. PUSH type (Broker) data providing  

When the data to be provides is required to be provided in real time, such as alerts for detecting intrusion, this method of providing is suitable. Vantiq makes a threshold judgment and then publishes the matched data to a broker. To use a fully managed service, AWS AmazonMQ or Azure Event Hubs are the available options. These brokers are easy to build, but there are some things to keep in mind. For example, the number of simultaneous connections of Event Hubs is determined by the settings. When using a fully managed service, it is necessary to understand the characteristics of the service itself before implementing it, although it is not limited only for brokers.

<a id="data-providing-summary"></a>
### 4.3. Summary of Data Providing Layer

For this layer, the implementation itself is not complicated, but the required performance and the scope of API exposure will differ depending on the requirements. Therefore, it is necessary to properly understand the characteristics of each cloud service and make the necessary settings.   
