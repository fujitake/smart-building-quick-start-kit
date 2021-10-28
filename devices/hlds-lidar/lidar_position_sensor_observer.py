'''
Prerequisites:
- HumanCounterPro.exe is already running.
- Among HumanCounterPro's functions, the target is "Tracking". Please check the manual if needed.
'''

import socket
import time
import datetime
import json
from struct import unpack_from
import paho.mqtt.client as mqtt
import os
from dotenv import load_dotenv

load_dotenv()

PUBLISH_INTERVAL_SEC = 10

# Lidar position sensor
SENSOR_ID = 'lidar_position_sensor1'
SOCKET_HOST = '127.0.0.1'
SOCKET_PORT = 6666 #  This port is for "Tracking".
BUFFER_SIZE = 19256 # Max size of tracking data.
BACKLOG = 1 # Number of clients that can be connected at the same time.

def publish_to_mqtt_broker(data):
    client = mqtt.Client()
    client.username_pw_set(os.getenv('MQTT_USER'), password=os.getenv('MQTT_PASSWORD'))
    client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLSv1_2, ciphers=None)
    client.tls_insecure_set(True)
    client.connect(os.getenv('MQTT_HOST'), 8883)
    client.publish(os.getenv('MQTT_TOPIC'), json.dumps(data))
    print('Published Event: ' + datetime.datetime.fromtimestamp(time.time()).strftime('%Y/%m/%d %H:%M:%S'))
    client.disconnect()

def parse_store_human_data(data):
    common_header_length = 56
    seek = 0
    total_size = unpack_from('<I', data, seek)[0]
    total_count_data_length = total_size - common_header_length
    seek += 4
    format_type = unpack_from('<I', data, seek)[0]
    seek += 4
    format_version = unpack_from('<Q', data, seek)[0]
    seek += 8
    frame_id = unpack_from('<Q', data, seek)[0]
    seek += 8
    timestamp = unpack_from('<16c', data, seek)[0]
    seek += 16
    time_ms = unpack_from('<Q', data, seek)[0]
    seek += 8
    track_num = unpack_from('<I', data, seek)[0]
    seek += 4
    rcv = unpack_from('<I', data, seek)[0]
    seek += 4

    people_locations = []
    while seek < total_count_data_length:
        human_id = unpack_from('<Q', data, seek)[0]
        seek += 8
        x = unpack_from('<f', data, seek)[0]
        seek += 4
        y = unpack_from('<f', data, seek)[0]
        seek += 180
        person_location = {
            'x': x,
            'y': y
        }
        people_locations.append(person_location)

    result = {
       'people_num': len(people_locations),
       'people_locations': people_locations
    }
    return result

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((SOCKET_HOST, SOCKET_PORT))
        s.listen(BACKLOG)
        while True:
            try:
                client, addr = s.accept()
                with client as c:
                    data = c.recv(BUFFER_SIZE)
                    data = parse_store_human_data(data)
                    data['sensor_id'] = SENSOR_ID
                    print(data)
                    publish_to_mqtt_broker(data)
            except KeyboardInterrupt:
                break
            except Exception as e: 
                print('[Error] ' + str(e.args))
            finally:
                time.sleep(PUBLISH_INTERVAL_SEC)   

if __name__ == '__main__':
    main()