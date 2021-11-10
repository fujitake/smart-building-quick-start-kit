[Japanese](./README.md)

# Hitachi LG LiDAR Sensor (HLS-LFOM5)

### **Overview and Prerequisite**
---
This is the procedure to send the information sensed by the LiDAR sensor to an MQTT broker.

This procedure uses two types of sensing contents: `positions of people` and `counting the number of people crossed lines`.

This also describes the minimum required steps from activating LiDAR sensor to sending sensing results to an MQTT broker. Please refer to the LiDAR sensor manuals in details such as settings for multiple sensors, kitting and etc.

### **Required items**
---
- Hitachi LG LiDAR Sensor（this procedure uses one HLS-LFOM5)
- Windows 10 PC (To run software for the LiDAR Sensor)  
- Sample scripts (To get sensed results via socket communication and send them to an MQTT broker)  
    - For `positions-of-people` data
        - lidar_position_sensor_observer.py
            - Sends positions of people data to an MQTT broker.
    - For `number-of-people-who-crossed-lines` data
        - lidar_inout_sensor_observer.py
            - Sends each number of people who crossed IN line and OUT line to an MQTT broker.

- MQTT broker

### **Outline**
---
1. Prepare an MQTT broker.
1. Prepare Hitachi-LG LiDAR sensor and a Windows PC on the same network as the sensor.  
1. Install SDK for LiDAR sensor and  **People Tracking** package on a Windows PC.  
1. Execute the application included in the People Tracking package.  
1. Execute the sample scripts.  


## **Procedure**
### 1. Prepare MQTT broker  
---
Prepare any MQTT broker (such as a fully managed one like AmazonMQ or build yourself with Mosquito).

<br/>


### 2. Set up Windows PC
---
1. Install SDK
    1. Download the latest SDK for Windows from the [download page](https://hlds.co.jp/product-eng/tofsdk)(e.g.: `HldsTofSdk.2.3.0vs2015.zip`).
    
        ※ When using Google Chrome, downloading can fail. In that case, change the browser.
    1. Unzip the downloaded zip file and run the driver installer.
    
        e.g.: ``HldsTofSdk.2.3.0vs2015\x64\tofdriver\tof_driver_x64_v2.3.0_Installer``

    ※ Please check the enclosed manuals if errors occur while running the installer.
    `HldsTofSdk.2.3.0vs2015\manual`
1. Download People Tracking package
    1. Download the latest version from the [download page](https://hlds.co.jp/product/tofsdk/people-tracking_en)(e.g.: `PeopleTracking_v200.zip`).
    1. Unzip the downloaded zip file at any location.  

<br/>

### 3. Change LiDAR sensor settings  
---
1. Change IP Address
    1. Open `http://<IP address of the LiDAR sensor>` with a browser to access the console screen.
        1. Initial IP: `192.168.0.105`, Initial Password: `admin`
    1. Open the network settings menu, and change the IP address to the same network as the Windows terminal.  
        1. Also, copy the MAC address.  

<br/>


### 4. Execute HumanCounterPro (People Tracking application).  
---
HumanCounterPro settings are described in the XML files (`Store*.xml, HumanCounterPro.xml`) that exist in `PeopleTracking_v200\PeopleTracking`, and these XML files are read when the application is started. So, you can set this application by modifying these XML files.

In this procedure, modify `StoreTof.xml` and `HumanCounterPro.xml`, which are the minimum required.

(You don't need to modify these files if you just would like to run HumanCounterPro.exe. this step is necessary for socket communication.)


<br/>

1. Set the IP address and the MAC address of the LiDAR sensor in `StoreTof.xml`.
```xml:StoreTof.xml
...
    <Tof>
        <PcNo>1</PcNo>
        <TofNo>1</TofNo>
        <Mac>MAC address of the LiDAR Sensor</Mac>　← Revise this value
        <Ip>IP address of the LiDAR Sensor</Ip>　← Revise this value
        <Height>2260</Height>
        <AngleX>72</AngleX>
        <AngleY>0</AngleY>
        <AngleZ>87</AngleZ>
        <Direction>161</Direction>
        ...
...
```
2. Enable the socket outputs of two types of data in ``HumanCounterPro.xml``: `StoreHuman (Tracking data)` and `HumanCount (Line Counting data)`.  
```xml:HumanCounterPro.xml
...
    <Output>
        <StoreHuman>
            <Valid>1</Valid> ← Set "1" ("0" is disabled)
            <Socket>
                <Valid>1</Valid> ← Set "1"
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
            <Valid>1</Valid> ← Set "1"
            <PeriodSec>60</PeriodSec>
            <Socket>
                <Valid>1</Valid> ← Set "1"
                <Ip>127.0.0.1</Ip>
                <Port>6667</Port>
            </Socket>
            <File>
                <Valid>0</Valid>
            </File>
        </HumanCount>
        ...
...
```

3. 【***This step is for HumanCount (Line Counting data). you don't need to do it when not using HumanCount***】Use `TofStitcher.exe` to draw lines.  

    Since HumanCount is data that counts the number of people who crossed lines, so it requires setting lines beforehand.

    You can draw virtual lines by using `TofStitcher.exe` included in the People Tracking package.

    1. Draw two lines, one is for IN and another is for OUT.
        1. Please refer to the enclosed `HLDS_TOF_TofStitcher_Operation_Manual.pdf` for details about how to use `TofStitcher.exe`.
    1. Edit `<Count>/<CountName>` in `StoreCount.xml`, revise the names of count groups for IN and for OUT according to the following naming rules.  
    ```
    For IN： <Any alphanumeric name>_in
    For OUT： <Any alphanumeric name>_out
    ```
    ```xml:StoreCount.xml
    ...
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
    ...
    ```

1. Execute `HumanCounterPro.exe`.

1. Confirm that socket communication is enabled.
    1. Execute `PeopleTracking_v200\SocketReceiver\ReceiveTest.exe` to confirm that the data can be received.

<br/>

### 5. Send sensing results to MQTT broker 
---
1.  Place the sample scripts on the Windows PC.  
    - `lidar_position_sensor_observer.py`
    - `lidar_inout_sensor_observer.py`

1. Create a `.env` file in the same directory as the sample scripts, and set your MQTT broker information.
```.env
MQTT_HOST = 'your-broker.com'
MQTT_TOPIC = '/lidar/position' → For using "lidar_position_sensor_observer.py"  
# MQTT_TOPIC = '/lidar/inout' → For using "lidar_inout_sensor_observer.py"
MQTT_USER = 'your-username'
MQTT_PASSWORD = 'your-password'
```

2.  Execute `lidar_*_sensor_observer.py`.  

>Check the script, and if there are any modules that are not installed in your environment, install the necessary ones.  

> HumanCounterPro.exe has to be running.

Send `positions-of-people` data.  
```
$ python lidar_position_sensor_observer.py
```
Send `number-of-people-who-crossed-lines` data.
```
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
