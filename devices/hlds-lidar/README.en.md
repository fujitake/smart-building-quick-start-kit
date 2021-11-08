[Japanese](./README.md)

# Hitachi LG LiDAR Sensor (HLS-LFOM5)  

### **Overview and Prerequisite**
---
This is the instructions to send the contents that are sensed by the LiDAR sensor to an MQTT broker. In these  instructions, two types of sensing contents will be used: "location of persons" and "counting the number of persons who crossed the line".<br/>
It also describes the minimum required instructions from LiDAR sensor startup to transmission to an MQTT Broker. As for the individual instructions for multiple types of LiDAR sensors, settings for when operating multiple sensors, kitting, etc., please refer to the LiDAR sensor manual.  

### **Requirements for these instructions.**
---
- Hitachi LG LiDAR Sensor（In these instructions, one HLS-LFOM5 is used.）  
- Windows 10 terminal (To run the software for the LiDAR Sensor.)  
- Set of the scripts in this directory (To execute socket communication and send the acquired data to an MQTT Broker.)  
    - Send the "location of persons" data to an MQTT Broker.  
        - lidar_position_sensor_observer.py
            - The script that sends the "location of persons" data to an MQTT Broker.  
    - Send the "counting the number of persons who crossed the line" data to an MQTT Broker.  
        - lidar_inout_sensor_observer.py
            - The Script that sends the data of the number of persons who crossed two lines, one is for IN and another is for OUT, to an MQTT Broker.  

- An MQTT Broker

### **Overall flow of the work**
---
1. Prepare an MQTT Broker.
1. Prepare Hitachi-LG LiDAR sensor and a Windows terminal on the same network as the sensor.  
1. Install the SDK for the LiDAR sensor and the package for the **People Tracking** (the flow line measurement) on a Windows terminal.  
1. Execute the application included in the People Tracking package.  
1. Execute the Python scripts.  


## **Instructions**
### 1. Prepare an MQTT Broker.  
---
Prepare an MQTT Broker of any choice, such as a fully managed one like AmazonMQ or build your own with Mosquito.  

<br/>


### 2. Set up the Windows terminal.  
---
1. Install the SDK  
    1. Download the latest SDK for Windows from the [download page](https://hlds.co.jp/product-eng/tofsdk). (e.g., HldsTofSdk.2.3.0vs2015.zip) <br/> ※ When using Google Chrome, it may not be able to download. In that case, change the browser.  
    1. Unzip the zip file and run the driver installer.  　
    <br/> 例 ``HldsTofSdk.2.3.0vs2015\x64\tofdriver\tof_driver_x64_v2.3.0_Installer``

    ※ If an error occurs when running the installer, confirm the handling method in the enclosed manual.  
    ``HldsTofSdk.2.3.0vs2015\manual``
1. Download the People Tracking package.  
    1. Download the latest version from the [download page](https://hlds.co.jp/product/tofsdk/people-tracking_en). (e.g., PeopleTracking_v200.zip)  
    2. Unzip the zip file at any location.  

<br/>

### 3. Change the configuration of the LiDAR sensor.  
---
1. Change the IP Address  
    1. Open ``http://<IP address of the LiDAR sensor>`` in a browser to access the console screen.  
        1. Initial IP: ``192.168.0.105``, Initial Password: ``admin``
    1. Open the Network Settings menu, and change the IP address to the same network as the Windows terminal.  
        1. Also, copy the MAC address.  

<br/>


### 4. Execute the HumanCounterPro (the People Tracking application).  
---

The configuration of HumanCounterPro is described in the XML files that exist in ``PeopleTracking_v200\PeopleTracking`` (``Store*.xml`` and ``HumanCounterPro.xml``). Since these XML files are loaded when the application is launched, it is possible to do any configuration by modifying these XML files. In these instructions, modify the required ``StoreTof.xml`` and ``HumanCounterPro.xml`` (it is not necessary if just running HumanCounterPro.exe, but it is necessary in case of doing socket communication).  

<br/>

1. Configure the IP address and the MAC address of the LiDAR sensor in ``StoreTof.xml``.
```xml:StoreTof.xml
...(omitted)...
    <Tof>
        <PcNo>1</PcNo>
        <TofNo>1</TofNo>
        <Mac>MAC address of the LiDAR Sensor</Mac>　← revise this value
        <Ip>IP address of the LiDAR Sensor</Ip>　← revise this value
        <Height>2260</Height>
        <AngleX>72</AngleX>
        <AngleY>0</AngleY>
        <AngleZ>87</AngleZ>
        <Direction>161</Direction>
        ...
...(omitted)...
```
2. Enable the socket output of two types of data in ``HumanCounterPro.xml``: "StoreHuman (Tracking data)" and "HumanCount (Line Counting data)".  
```xml:HumanCounterPro.xml
...(omitted)...
    <Output>
        <StoreHuman>
            <Valid>1</Valid> ← set the value to "1"  ※ If it is "0", it means disable.
            <Socket>
                <Valid>1</Valid> ← set the value to "1"
                <Ip>127.0.0.1</Ip>
                <Port>6666</Port>
            </Socket>
            <File>
                <Valid>0</Valid>
                <PeriodMin>60</PeriodMin>
                <ReduceStandLog>0</ReduceStandLog>
            </File>
        </StoreHuman>
        <HumanCount>
            <Valid>1</Valid> ← set the value to "1"
            <PeriodSec>60</PeriodSec>
            <Socket>
                <Valid>1</Valid> ← set the value to "1"
                <Ip>127.0.0.1</Ip>
                <Port>6667</Port>
            </Socket>
            <File>
                <Valid>0</Valid>
            </File>
        </HumanCount>
        ...
...(omitted)...
```

3. ***In case of using HumanCount (Line Counting data), follow these instructions.***   
   Use `TofStitcher.exe` to draw a line.  

     HumanCount is the data that counts the number of persons who crossed the line, so it is necessary to configure the lines in advance. It is possible to configure the line settings with ``TofStitcher.exe`` included in the People Tracking package.  
     1. Configure a total of two lines, one is for IN and another is for OUT, using ``TofStitcher.exe``.  
        1. Please refer to the enclosed ``HLDS_TOF_TofStitcher_Operation_Manual.pdf`` for detailed instructions on how to use ``TofStitcher.exe``.  
     1.  In ``<Count>/<CountName>`` of ``StoreCount.xml``, revise the names of the count groups for IN and for OUT according to the following naming rules.  
    ```
    For IN： <Any alphanumeric name>_in
    For OUT： <Any alphanumeric name>_out
    ```
    ```xml:StoreCount.xml
    ...(omitted)...
        <!-- e.g., For IN -->
        <Count>
            <CountName>entrance_1_in</CountName> ← revise this value
            <Line>
                <LineName>Line-1</LineName>
                <Left>
                    <x>5060</x>
                    <y>4449</y>
                </Left>
                <Right>
                    <x>8224</x>
                    <y>2501</y>
                </Right>
            </Line>
            <Attribute>NULL</Attribute>
        </Count>
        ...
    ...(omitted)...
    ```

1. Execute ``HumanCounterPro.exe``.  
    1. Confirm that it launches.   

1. Confirm that socket communication is possible.  
    1. Execute ``PeopleTracking_v200\SocketReceiver\ReceiveTest.exe`` to confirm that the data can be received.

<br/>

### 5. Send the sensing results to the MQTT Broker.  
---
1.  Place the set of the scripts on the Windows terminal.  
    - ``lidar_position_sensor_observer.py``
    - ``lidar_inout_sensor_observer.py``

1.  Create a ``.env`` file in the same directory as the set of the scripts, and configure the information about your MQTT broker.  
```.env
MQTT_HOST = 'your-broker.com'
MQTT_TOPIC = '/lidar/position' → For using "lidar_position_sensor_observer.py"  
# MQTT_TOPIC = '/lidar/inout' → For using "lidar_inout_sensor_observer.py"
MQTT_USER = 'your-username'
MQTT_PASSWORD = 'your-password'
```

2.  Execute ``lidar_*_sensor_observer.py``.  

>Check the script, and if there are any modules that are not installed in your environment, install the necessary ones.  
```
※ HumanCounterPro.exe should be running.  

Send the "location of persons" data.  
$ python lidar_position_sensor_observer.py

Send the "counting the number of persons who crossed the line" data.  
$ python lidar_inout_sensor_observer.py
```

**Output Specifications**

- lidar_position_sensor_observer.py

|Items|Details|
|---|---|
|Protocol|MQTTS|
|Frequency| Depends on the output frequency setting of the LiDAR sensor |
|Format|JSON |

**Output sample**
```JSON
{
   "people_num": 2,
   "people_locations": [
      {
         "x": 7581.236328125,
         "y": 3981.5244140625
      },
      {
         "x": 6982.72509765625,
         "y": 4751.01220703125
      }
   ],
   "sensor_id": "lidar_position_sensor1"
}
```

- lidar_inout_sensor_observer.py

|Items|Details|
|---|---|
|Protocol|MQTTS|
|Frequency| Depends on the output frequency setting of the LiDAR sensor |
|Format|JSON |

**Output sample**
```JSON
{
   "count_data_list": [
      {
         "id": "vantiq",
         "in": 1,
         "out": 0
      }
   ],
   "sensor_id": "lidar_inout_sensor1"
}
```
