[English](./README.en.md)

# 円形メーターリーダー

## 概要・前提

円形のメーターの値を読み取り、MQTTブローカーに読み取った値を送信する手順です。

値の読み取りの精度を高くしたい場合はカメラに円形メーターのみがピントが合った状態で大きく写り、可能な限り影が少ないことが必要となります。

スマートビル化の過程を体験する目的で作成されているため、高い精度を求める場合には不向きです。

## 必要なもの
- 円形のメーター
    - 目盛りが複数種類ないこと（温度兼湿度計などでないこと）
    - [参考画像](#meter-image)
>スクリプト単体の動作として検出対象を温度計に限りませんが、Smart Building Quick Start Kitでは、温度計の読み取りとして使用します

- スクリプト
    - analog_round_meter_reader.py

> 本手順で使用するスクリプトは、サンプル画像でも動作させることができます。円形のメーターやRaspberry piなどがなくてもお試しいただけます。サンプル画像を使う処理はコメントアウトされておりますので、必要な場合は該当箇所のコメントを解除してください。

- PCおよびカメラ
    - 本手順ではRaspberry pi 4B + Picamera v2で動作を検証
- MQTT ブローカー


## 手順


1. スクリプトで使用する環境変数の設定

スクリプトと同じディレクトリに`.env`ファイルを作成し、自分のMQTTブローカーに関する情報と、円形メーターの最小値、最小値の角度、最大値、最大値の角度を設定する

```.env
# MQTT broker
MQTT_HOST = 'your-broker.com'
MQTT_PORT = 8883
MQTT_TOPIC = '/analog_meter/temperature'
MQTT_USER = "your-username"
MQTT_PASSWORD = 'your-password'

# Analog round meter
MIN_ANGLE = 80
MAX_ANGLE = 280
MIN_VALUE = -30
MAX_VALUE = 60
```
>**円形メーターに関する情報の設定方法**

<a id="meter-image"></a>

【参考画像】

<img src="./img/calibration.jpg" width="400">

参考画像の場合、設定情報は以下のようになる

```
MIN_ANGLE = 80  # 最小値の角度
MAX_ANGLE = 278 # 最大値の角度
MIN_VALUE = -25 # 最小値
MAX_VALUE = 55  # 最大値
```
>スクリプトを実行すると参考画像のようなメーターの周りに角度が表示されるため、一度試験的に任意の値でスクリプトを実行し、角度を把握してから設定するとスムーズです


2.  `analog_round_meter_reader.py`を実行する
>実行する前にスクリプトを確認し、自身の環境にインストールされていないモジュールがある場合は足りないものをインストールしてください
```
$ python analog_round_meter_reader.py
```


**出力の仕様**

|項目|内容|
|-|-|
|プロトコル|MQTTS|
|頻度|60秒ごとに1回|
|フォーマット|JSON |

```JSON
{
   "deviceId": "temp_meter_001",  # デバイスのID
   "temperature": 27.48 # 温度（℃）
}
```