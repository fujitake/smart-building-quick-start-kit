'''
The MIT License (MIT)
Copyright © 2014-2017 Intel Corporation
Copyright © 2021 Vantiq Inc.

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''
import cv2
import json
import numpy as np
import time, datetime
import paho.mqtt.client as mqtt
import os
from dotenv import load_dotenv

load_dotenv()

# Camera
VIDEO_SOURCE = 0

# Device
DEVICE_ID = 'temp_meter_001'
UNIT = '℃'
PUBLISH_INTERVAL_SEC = 60


def publish_to_mqtt_broker(data):
    client = mqtt.Client()
    client.username_pw_set(os.getenv('MQTT_USER'), password=os.getenv('MQTT_PASSWORD'))
    client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLSv1_2, ciphers=None)
    client.tls_insecure_set(True)
    client.connect(os.getenv('MQTT_HOST'), int(os.getenv('MQTT_PORT')))
    client.publish(os.getenv('MQTT_TOPIC'), json.dumps(data))
    print('Published Event: ' + datetime.datetime.fromtimestamp(time.time()).strftime('%Y/%m/%d %H:%M:%S'))
    client.disconnect()

def avg_circles(circles, b):
    avg_x=0
    avg_y=0
    avg_r=0
    for i in range(b):
        avg_x = avg_x + circles[0][i][0]
        avg_y = avg_y + circles[0][i][1]
        avg_r = avg_r + circles[0][i][2]
    avg_x = int(avg_x/(b))
    avg_y = int(avg_y/(b))
    avg_r = int(avg_r/(b))
    return avg_x, avg_y, avg_r

def dist_2_pts(x1, y1, x2, y2):
    return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def calibrate_gauge(frame):
    height, width = frame.shape[:2]
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, np.array([]), 100, 50, int(height*0.35), int(height*0.48))
    if circles.shape == (0,):
        x = y = r = None
    else: 
        a, b, c = circles.shape
        x,y,r = avg_circles(circles, b)

        cv2.circle(frame, (x, y), r, (0, 0, 255), 3, cv2.LINE_AA)  # draw circle
        cv2.circle(frame, (x, y), 2, (0, 255, 0), 3, cv2.LINE_AA)  # draw center of circle

        separation = 10.0 #in degrees
        interval = int(360 / separation)
        p1 = np.zeros((interval,2))
        p2 = np.zeros((interval,2))
        p_text = np.zeros((interval,2))
        for i in range(0,interval):
            for j in range(0,2):
                if (j%2==0):
                    p1[i][j] = x + 0.9 * r * np.cos(separation * i * 3.14 / 180) #point for lines
                else:
                    p1[i][j] = y + 0.9 * r * np.sin(separation * i * 3.14 / 180)
        text_offset_x = 10
        text_offset_y = 5
        for i in range(0, interval):
            for j in range(0, 2):
                if (j % 2 == 0):
                    p2[i][j] = x + r * np.cos(separation * i * 3.14 / 180)
                    p_text[i][j] = x - text_offset_x + 1.2 * r * np.cos((separation) * (i+9) * 3.14 / 180) #point for text labels, i+9 rotates the labels by 90 degrees
                else:
                    p2[i][j] = y + r * np.sin(separation * i * 3.14 / 180)
                    p_text[i][j] = y + text_offset_y + 1.2* r * np.sin((separation) * (i+9) * 3.14 / 180)  # point for text labels, i+9 rotates the labels by 90 degrees

        for i in range(0,interval):
            cv2.line(frame, (int(p1[i][0]), int(p1[i][1])), (int(p2[i][0]), int(p2[i][1])),(0, 255, 0), 2)
            cv2.putText(frame, '%s' %(int(i*separation)), (int(p_text[i][0]), int(p_text[i][1])), cv2.FONT_HERSHEY_SIMPLEX, 0.3,(0,0,0),1,cv2.LINE_AA)

        # cv2.imwrite('calibration.jpg', frame)

    return x, y, r

def get_current_value(frame, x, y, r):
    gray2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    thresh = 175
    maxValue = 255
    th, dst2 = cv2.threshold(gray2, thresh, maxValue, cv2.THRESH_BINARY_INV);
    minLineLength = 10
    maxLineGap = 0
    lines = cv2.HoughLinesP(image=dst2, rho=3, theta=np.pi / 180, threshold=100, minLineLength=minLineLength, maxLineGap=0)  # rho is set to 3 to detect more lines, easier to get more then filter them out later
    final_line_list = []

    diff1LowerBound = 0.15 #diff1LowerBound and diff1UpperBound determine how close the line should be from the center
    diff1UpperBound = 0.25
    diff2LowerBound = 0.5 #diff2LowerBound and diff2UpperBound determine how close the other point of the line should be to the outside of the gauge
    diff2UpperBound = 1.0

    for i in range(0, len(lines)):
        for x1, y1, x2, y2 in lines[i]:
            diff1 = dist_2_pts(x, y, x1, y1)  # x, y is center of circle
            diff2 = dist_2_pts(x, y, x2, y2)  # x, y is center of circle
            #set diff1 to be the smaller (closest to the center) of the two), makes the math easier
            if (diff1 > diff2):
                temp = diff1
                diff1 = diff2
                diff2 = temp

            if (((diff1<diff1UpperBound*r) and (diff1>diff1LowerBound*r) and (diff2<diff2UpperBound*r)) and (diff2>diff2LowerBound*r)):
                final_line_list.append([x1, y1, x2, y2])

    x1 = final_line_list[0][0]
    y1 = final_line_list[0][1]
    x2 = final_line_list[0][2]
    y2 = final_line_list[0][3]
    cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # cv2.imwrite('needle.jpg', frame)

    dist_pt_0 = dist_2_pts(x, y, x1, y1)
    dist_pt_1 = dist_2_pts(x, y, x2, y2)
    if (dist_pt_0 > dist_pt_1):
        x_angle = x1 - x
        y_angle = y - y1
    else:
        x_angle = x2 - x
        y_angle = y - y2

    res = np.arctan(np.divide(float(y_angle), float(x_angle)))
    res = np.rad2deg(res)
    if x_angle > 0 and y_angle > 0:  #in quadrant I
        final_angle = 270 - res
    if x_angle < 0 and y_angle > 0:  #in quadrant II
        final_angle = 90 - res
    if x_angle < 0 and y_angle < 0:  #in quadrant III
        final_angle = 90 - res
    if x_angle > 0 and y_angle < 0:  #in quadrant IV
        final_angle = 270 - res

    old_min = float(os.getenv('MIN_ANGLE'))
    old_max = float(os.getenv('MAX_ANGLE'))

    new_min = float(os.getenv('MIN_VALUE'))
    new_max = float(os.getenv('MAX_VALUE'))

    old_value = final_angle

    old_range = (old_max - old_min)
    new_range = (new_max - new_min)
    new_value = (((old_value - old_min) * new_range) / old_range) + new_min

    return new_value


def main():
    cap = cv2.VideoCapture(VIDEO_SOURCE)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('H', '2', '6', '5')) 
    last_published_time = time.time() - PUBLISH_INTERVAL_SEC
    while True:
        try:
            ret, frame = cap.read()
            x, y, r = calibrate_gauge(frame)
            if x != None and y != None and r != None: 
                val = get_current_value(frame, x, y, r)
                val = round(val,2)
                print("Current temperature: %s %s" %(val, UNIT))
                cv2.putText(frame, 'Current temperature:', (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                cv2.putText(frame, str(val), (10,45), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                now = time.time()
                if now - last_published_time > PUBLISH_INTERVAL_SEC:
                    data = {}
                    data['deviceId'] = DEVICE_ID
                    data['temperature'] = val
                    publish_to_mqtt_broker(data)
                    last_published_time = time.time()
            else:
                print('Round meter is not found.')
            cv2.namedWindow('VIDEO', cv2.WINDOW_NORMAL)
            cv2.imshow('VIDEO', frame)
            time.sleep(1)
        except Exception: 
            pass
        except KeyboardInterrupt:
            break
        key = cv2.waitKey(1)
        if key == 27:
            break
    cv2.destroyAllWindows()

if __name__=='__main__':
    main()