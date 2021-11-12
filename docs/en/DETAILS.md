[Japanese](../ja/DETAILS.md)

# Smart Building Quick Start Details

## Contents  

1. [Introduction](#introduction)
2. [Device Layer](#device-layer)

    2.1. [Device specification](#device-spec)

    2.1.1. [What can this device do](#what-can-device-do)

    2.1.2. [Device quality](#device-quality)

    2.1.3. [How to send data](#device-data-sending)

    2.1.4. [How to supply power](#device-power-supply)

    2.1.5. [Installation requirement](#device-installation)

    2.1.6. [Data specification](#device-data-spec)

    2.2. [Price](#device-price)

    2.3. [Laws and Regulations](#device-laws)

    2.4. [Data loss](#device-data-loss)

    2.5. [Data sending path to data integration layer (Vantiq)](#device-data-path)

    2.6. [Operation in abnormality/failure](#device-operation)

    2.7. [Summary of Device Layer](#device-summary)

3. [Data Integration Layer](#data-integration-layer)

    3.1. [Master data Management](#data-integration-master-data)

    3.2. [Data Store](#data-integration-data-store)

    3.3. [Vantiq](#data-integration-vantiq)

    3.3.1. [Frequently used Activity Patterns](#data-integration-activity)

    3.3.2. [Performance-considered implementation](#data-integration-performance)

    3.3.2.1. [Lighten processing per task](#data-integration-lighten)

    3.3.2.2. [Reduce/divide queries](#data-integration-reduce-queries)

    3.3.2.3. [Reduce simultaneous executions](#data-integration-reduce-simultaneous)

    3.3.2.4. [Verify actual performance](#data-integration-performacne-test)

    3.4. [Summary of Data Integration Layer](#data-integration-summary)

4. [Data Providing Layer](#data-providing-layer)

    4.1. [PULL type (API) data providing](#data-providing-pull)

    4.2. [PUSH type (Broker) data providing](#data-providing-push)

    4.3. [Summary of Data Providing Layer](#data-providing-summary)

<br />
<br />

<a id="introduction"></a>
## 1. Introduction

This document summarizes the details of the knowledge, concept and important points necessary to build a smart building with Vantiq. Smart building includes a wide range of elements, from devices to clouds, and not many people have an overall picture yet.

However, what you need to think about is, after all, the simple flow of how to collect, process, and provide data. It would be appreciated if you would read this document while being conscious of how can achieve that flow.

This content is just a basic pattern, so you will need to modify some parts according to your project/requirement, but the basic idea is same.

This document is constructed based on the each layer of the following figure:

<img src="../img/layers.en.png" width="1000">

<a id="device-layer"></a>
## 2. Device Layer

Devices are the most important element of all IoT projects, not just for smart building. Any plans can never be achieved without devices which can acquire necessary data.
In addition, device accuracy/precision is linked directly the entire system's data quality. In other words, making mistakes in device selection leads directly to the failure of the project itself. So you need to select them carefully.

Now let's move on to the device section.


<a id="device-spec"></a>
### 2.1. Device specification

You need to confirm the device specification in detail for judging whether the device can achieve what you'd like to achieve.

You'd better do this process carefully, even if it takes time. When devices are not suitable, the project will fail and waste time and money.

<a id="what-can-device-do"></a>
### 2.1.1. What can this device do

First of all, it's just obvious but, you need to know exactly what the device can do.

For example, even if you simply say "temperature sensor", you need to confirm &nbsp;`① what range of temperature it can measure (detection range)`, &nbsp;`② what unit it can measure (resolution)`, and &nbsp;`③ how much error may occur (accuracy)`.

You can't develop obviously the function of alerting when the temperature exceeds 100℃ if you selected a temperature sensor whose detection range is -30℃ to + 60℃.

Shouldn't think just like "this is a temperature sensor.". It's necessary to grasp in detail like "this temperature sensor can measure the detection range from -30℃ to + 60℃ in 0.1 ℃ increments and may have an error of about ± 0.2 ℃" firstly.

In addition, If you use devices that keep looking at a specific section such as AI cameras, it's important to confirm the coverage area by each device. It's strongly related to the total cost.


<a id="device-quality"></a>
### 2.1.2. Device quality

Frequent device failures, poor fire/water resistance and etc. can cause unexpected maintenance costs and accidents. 

It's very basic, but you should confirm the quality. It's safe to purchase 1 device and verify it actually before final selection, even from an aspect to verify the accuracy.

<a id="device-data-sending"></a>
### 2.1.3. How to send data

Confirm how to send the sensed data to another layer.

For example, if you'd like to use a temperature sensor, it doesn't make sense to just have a module with sensor elements, of course. Only after being used in combination with a micro-computer/IoT gateway(some devices include them), can send the data to another layer.

As for sending data way, it depends on devices:
- Used in combination with IoT gateway
- BLE connection
- Via a unique cloud service for the device
- Etc.
So, you need to confirm the way of your devices.

In case of using IoT gateway, you also need to confirm the path of after IoT gateway like WiFi or LTE.

<a id="device-power-supply"></a>
### 2.1.4. How to supply power

Whether a battery-powered device or not affects the installation position and maintainability. For smart building, battery-powered devices are not unlikely to be options, but it's safer to confirm.

<a id="device-installation"></a>
### 2.1.5. Installation requirement

There are two installation requirements meanings.

The first is device installation requirement. It means that under what circumstances(environment/condition) the device can perform like defined in the specification. You should confirm how to make devices perform correctly after understanding what devices can do because devices don't work well if you installed devices incorrectly. For example, even if you have an AI camera that can detect a human face with 100% accuracy, it doesn't work well when using it in a dark/too bright place where images quality will become low.  

The second installation requirement is from the building owner.
There are not many cases you can install your devices anywhere in the building as you like. It's necessary to install it the position permitted by the building side in consideration of the landscape and failure/replacement.

You'd better make sure the following thing: 
"I can achieve what I want to do with this device, but can this device install in an easy-to-maintain position of this building?"


<a id="device-data-spec"></a>
### 2.1.6. Data specification

Confirm protocol, format, size, and frequency of sending. Protocol and format will determine how can send the data to another layer. Size and frequency of sending affect the performance and implementation of the opposite system.

<a id="device-price"></a>
### 2.2. Price

Calculate the total price of the number of devices, IoT gateways, WiFi routers, SIM cards, and other necessary items and confirm whether the cost is worth it. Some devices need to use a unique cloud service for that device to send data, you may need to consider the cost of that kind of service also.

<a id="device-laws"></a>
### 2.3. Laws and Regulations

You have to be careful when using devices from overseas. It may be developed based on laws and regulations from your country. Devices must comply with the laws of your country. 

In addition, you also have to be careful when handling sensitive data like including personal information.


<a id="device-data-loss"></a>
### 2.4. Data loss

Especially in the case of wireless connection, data loss will occur, so it is necessary to consider measures such as increasing the number of devices to reduce the loss rate, complementing on the application side, and designing so that not be affected by data loss. 

<a id="device-data-path"></a>
### 2.5. Data sending path to data integration layer (Vantiq)

You need to consider how to send data from devices to Vantiq in the data integration layer. There are 2 main patterns.
The first is to use Vantiq REST API. The second is via broker with protocols such as MQTT, AMQP, and Kafka. 

First, when using Vantiq REST API, Devices must set the Vantiq access token in the header when making HTTP requests. You can use this way if your devices have this function. In some cases, a device can make HTTP requests, but not be able to set the header. In this case, you can use the Vantiq REST API by relaying the data with AWS Lambda/Azure Functions. (The device just makes a request to Lambda/Functions, then Lambda/Functions that hold the Vantiq access token make a request to Vantiq.)

Using REST API is simple/easy, but it has the following disadvantages:

1. Manage access token are complicated

    Since access tokens are embedded in the device side, you may need to replace tokens for all devices if it has to be updated due to expiration or leak. It depends on how tokens were distributed, but it's tough.

2. Impact on Vantiq performance

    Since HTTP is not lightweight, It consumes a lot of Vantiq resources if you use a large amount devices.

Secondly, if you select the way via a broker, no need to distribute access tokens (but the broker's authentication information is required).
In addition, MQTT, AMQP, and Kafka which are lighter than HTTP can be used. The disadvantages are the followings:

1. Need to prepare broker

    For example, you need to prepare AWS AmazonMQ/Azure Event Hubs and also need to understand the characteristics of these brokers specifically performance and required settings.

2. Difficulty of protocol support

    Protocol support is more difficult than HTTP. About the Vantiq side, these protocol's clients are already prepared in advance, but not many devices/IoT gateways support MQTT, AMQP, and Kafka even if they support HTTP.

In summary, it's easier to operate via broker unless you use extremely few devices. 

It's necessary to build brokers, but you can use a fully managed one, and if you manage devices with AWS IoT Core or Azure IoT hub, you can route data from devices to brokers. Therefore, it's easy to support the protocols.

**About device management service**

>You may see the services that state "device management" often, but what is "device" in this context? They never say "sensor management". These services can manage devices connected to the internet only. So to be precise, they are "IoT gateway management". Even if the IoT gateway can be managed, it can't manage the sensors connected to it (of course, in the case of devices that have both the sensing part and IoT gateway function, there is no problem). In any case, you should make a decision to the introduction that kind of service after understanding what the service can do.


<a id="device-operation"></a>
### 2.6. Operation in abnormality/failure

There is no machine never breaks. So any device will fail or be in an abnormal state someday.
The system had better be designed to identify abnormal devices and support device replacement.

<a id="device-summary"></a>
### 2.7. Summary of Device Layer

As this is the most important layer, there are many things to confirm. To summarize simply, the following should be confirmed:

1. Being possible to acquire the data to accomplish the plan/project.
1. Paths have been established to send the retrieved data to Vantiq.  
1. Being in a state that can be continuously operated.

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
### 3.3.2. Performance-considered implementation  

Vantiq can provide a high performance platform, but it may not be able to provide the performance depending on how it is implemented. It requires to understand the characteristics of Vantiq and to implement it accordingly. Especially, be more careful for those who are used to implementing web applications. Vantiq has the elements such as web (or mobile) client, DB, and application, so it is possible to implement 3-tier architecture for a traditional  web applications.
However, it is a service that specializes in stream processing, so applying in the common sense of web application development as is will result in failure.
It should be considered as an asynchronous and parallel processing of small processes at high speed.  

<a id="data-integration-lighten"></a>
### 3.3.2.1. Lighten processing per task

When implementing an application, it is necessary to lighten the content to be processed per task. When using Procedure, any number of processes can be grouped together and called in a single task. However, since Vantiq performs load balancing in units of one task, performance will be improved by dividing it into multiple tasks rather than executing heavy processing in one task. Typical heavy processing is that which needs to wait for the response of a system other than Vantiq, such as issuing SQL that cannot be completed in memory alone, or executing an external API.  

<a id="data-integration-reduce-queries"></a>
### 3.3.2.2. Reduce/divide queries

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
### 3.3.2.3. Reduce simultaneous executions

Trying to process a large amount of data all at once with less than a 0.1 second latency, it will consume a lot of resources at once. Therefore, the process needs to be shifted as slightly as possible. Vantiq has ***Scheduled Event***, but when using it to issue a large number of queries at the exact same time, the entire cluster will be overloaded.  

<a id="data-integration-performacne-test"></a>
### 3.3.2.4. Verify actual performance

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
