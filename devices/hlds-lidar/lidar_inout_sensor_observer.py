'''
Prerequisites:
- HumanCounterPro.exe is already running.
- Among HumanCounterPro's functions, the target is "Line Counting". Please check the manual if needed.
'''
import socket
import time
import datetime
import json
import re
from struct import unpack_from
import paho.mqtt.client as mqtt
import os
from dotenv import load_dotenv

load_dotenv()

PUBLISH_INTERVAL_SEC = 0

# Lidar inout sensor configuration
SENSOR_ID = 'lidar_inout_sensor1'
SOCKET_HOST = '127.0.0.1'
SOCKET_PORT = 6667 #  This port is for "Line Counting".
BUFFER_SIZE = 8872 # Max size of line counting data.
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

def parse_human_count_data(data):
    common_header_length = 72
    seek = 0
    total_size = unpack_from('<I', data, seek)[0]
    total_count_data_length = total_size - common_header_length
    seek += 4
    format_type = unpack_from('<I', data, seek)[0]
    seek += 4
    format_version = unpack_from('<Q', data, seek)[0]
    seek += 8
    format_id = unpack_from('<Q', data, seek)[0]
    seek += 8
    timestamp = unpack_from('<16c', data, seek)[0]
    seek += 16
    time_ms = unpack_from('<Q', data, seek)[0]
    seek += 8
    count_num = unpack_from('<i', data, seek)[0]
    seek += 4
    rcv = unpack_from('<I', data, seek)[0]
    seek += 4
    start_ms = unpack_from('<Q', data, seek)[0]
    seek += 8
    end_ms = unpack_from('<Q', data, seek)[0]
    seek += 8

    tmp_count_data = {}
    count_data_list = []
    while seek < total_count_data_length:
        countid = unpack_from('<Q', data, seek)[0]
        seek += 8
        countlabel = str(unpack_from('<64s', data, seek)[0].decode())
        seek += 64
        value = unpack_from('<Q', data, seek)[0]
        seek += 8
        accumulated = unpack_from('<Q', data, seek)[0]
        seek += 8

        count_id = re.search(r'[0-9a-zA-Z]+[^_in|^_out]', countlabel).group()
        if re.search(r'[0-9a-zA-Z]+_in', countlabel):
            tmp_count_data['id'] = count_id
            tmp_count_data['in'] = accumulated
        elif re.search(r'[0-9a-zA-Z]+_out', countlabel):
            tmp_count_data['id'] = count_id
            tmp_count_data['out'] = accumulated

        if 'id' in tmp_count_data and 'in' in tmp_count_data and 'out' in tmp_count_data:
            count_data_list.append(tmp_count_data)
            tmp_count_data = {}

    result = {
       'count_data_list': count_data_list
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
                    data = parse_human_count_data(data)
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