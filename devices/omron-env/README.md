[English](./README.en.md)

# オムロン環境センサー（2JCIE-BU01）

オムロン環境センサーから周辺環境に関する値を取得し、MQTTローカーに送信する手順です。


## 仕様

### 取得できる値

オムロン環境センサーには2種類あり、2JCIE-BU01(USB型)と2JCIE-BL01（バッグ型）それぞれで取得できる値に若干の差がありますが、温度、湿度、気圧など周辺環境に関する情報を取得できます。詳細はマニュアルをご確認ください。

本手順では`eCO2`を取得することができる`2JCIE-BU01(USB型)`を使用します。

- [形 2JCIE-BU01 環境センサ ユーザーズマニュアル(pdf)](https://omronfs.omron.com/ja_JP/ecb/products/pdf/CDSC-016A-web1.pdf)

- [形 2JCIE-BL01 環境センサ ユーザーズマニュアル(pdf)](https://omronfs.omron.com/ja_JP/ecb/products/pdf/CDSC-015.pdf)  


## セットアップ

### 必要なもの

- オムロン環境センサー（2JCIE-BU01）

- Raspberry Pi 3B+ または 4B
  - [Raspberry Pi OS with desktop (32bit)](https://www.raspberrypi.org/software/operating-systems/#raspberry-pi-os-32-bit)
  - 必ずしもRaspberry piを使用する必要はございませんが、本手順の検証では Raspberry Pi 3B+及び4Bを使用しています。

- 本ディレクトリ一式

### 手順

1. 環境センサーの Mac アドレスの確認

```
$ sudo hcitool lescan
LE Scan ...
C2:B7:E4:CC:FE:79 Env
※「Env」が環境センサーのMacアドレス
```


2. Raspberry Pi の任意のディレクトリに `envsensor_observer.py` を配置します
3. 秘匿情報等は環境変数としてスクリプトへ読み込みます  
   `.env.sample` ファイルをコピーして `.env` ファイルを作成し、ファイル内の説明に沿った値を設定してください

4. 必要なパッケージ、モジュールをインストールします
envsensor_observer.py と同じディレクトリに`requirements.txt` ファイルを設置し、アプリケーションに必要な Python モジュールをインストールします

```
$ sudo apt install libglib2.0-dev
$ pip3 install -r requirements.txt
```

## 実行

envsensor_observer.py を実行し、データが送信されることを確認します

```
$ python3 envsensor_observer.py
Published Event: 2021/09/21 11:03:46
{'pressure': 1005, 'noise': 42, 'temperature': 29, 'env_sensor_id': 'env_sensor1', 'etvoc': 3, 'light': 44, 'eco2': 422, 'humidity': 55}
```

## 送信詳細

| 項目         | 内容                  |
| ------------ | --------------------- |
| プロトコル   | MQTTS                 |
| 頻度         | 10 秒ごとに 1 回送信  |
| フォーマット | JSON                  |

**出力サンプル**
```
{
	"env_sensor_id": "env_sensor1",
	"pressure": 1005,
	"noise": 42,
	"temperature": 29,
	"etvoc": 3,
	"light": 44,
	"eco2": 422,
	"humidity": 55
}
```

## 注意点

- 環境センサーと Raspberry Pi を 1m 以内の距離で設置してください。
- MQTT Broker との通信経路の暗号化・認証は簡易的なものなので、実際の案件で求められるセキュリティレベルに応じて対策ください。
