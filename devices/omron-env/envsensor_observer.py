import datetime
import json
import os
import struct
import time

import paho.mqtt.client as mqtt
from bluepy import btle
from dotenv import load_dotenv

PUBLISH_INTERVAL_SEC = 10

load_dotenv()

def publish_event(data):
    client = mqtt.Client()
    client.username_pw_set(os.getenv("MQTT_USER"), password=os.getenv("MQTT_PASSWORD"))
    client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLSv1_2, ciphers=None)
    client.tls_insecure_set(True)
    client.connect(os.getenv("MQTT_BROKER_HOST"), 8883)
    client.publish(os.getenv("MQTT_TOPIC"), json.dumps(data))
    client.disconnect()
    print(
        "Published Event: "
        + datetime.datetime.fromtimestamp(time.time()).strftime("%Y/%m/%d %H:%M:%S")
    )


def get_env_sensor_data():
    peripheral = btle.Peripheral(os.getenv("ENV_SENSOR_MAC_ADDRESS"), addrType=btle.ADDR_TYPE_RANDOM)
    characteristic = peripheral.readCharacteristic(0x0059)
    seq, temp, humid, light, press, noise, etvoc, eco2 = struct.unpack('<Bhhhlhhh', characteristic)
    data = {
            'env_sensor_id': os.getenv("ENV_SENSOR_ID"),
            'temperature': temp / 100,
            'humidity': humid / 100,
            'light': light,
            'pressure': press / 1000,
            'noise': noise / 100,
            'etvoc': etvoc,
            'eco2': eco2
        }
    return data

def main():
    while True:
        try:
            data = get_env_sensor_data()
            publish_event(data)
            print(data)
        except KeyboardInterrupt:
            break
        except btle.BTLEDisconnectError:
            print('Disconnected: ' + datetime.datetime.fromtimestamp(time.time()).strftime('%Y/%m/%d %H:%M:%S'))
        time.sleep(PUBLISH_INTERVAL_SEC)


if __name__ == "__main__":
    main()
