[English](./README.en.md)

# 日立LG LiDARセンサー（HLS-LFOM5）

### **概要・前提**
---
LiDARセンサーによってセンシングした内容をMQTTブローカーに送信するまでの手順です。本手順では、「人の位置」「ラインを跨いだ人数のカウント」の2種類のセンシング内容を使用します。<br/>
また、LiDARセンサー起動からVantiqに送信するまでの最低限の手順を記載しています。複数種類あるLiDARセンサー個別の手順、複数台運用する場合の設定、キッティングなどについてはLiDARセンサーのマニュアルをご確認ください。

### **必要なもの**
---
- 日立LG LiDARセンサー（本手順ではHLS-LFOM5を1台使用）
- Windows 10の端末（LiDARセンサー用のソフトウェアを動作させる）
- スクリプト一式（ソケット通信を行い、取得したデータをVantiqに送信する）
    - 「人の位置」のデータをVantiqに送信
        - lidar_position_sensor_observer.py
            - 人の位置データをVantiqに送信するスクリプト
    - 「ラインを跨いだ人数のカウント」のデータをVantiqに送信
        - lidar_inout_sensor_observer.py
            - IN用、OUT用の2つのラインを跨いだ人数のデータをVantiqに送信するスクリプト

- MQTTブローカー

### **作業の大まかな流れ**
---
1.  MQTTブローカーの準備
1.  日立LG社のLiDARセンサーと同ネットワーク上にWindows端末を用意
1.  Windows端末にLiDARセンサー用のSDK及び動線計測のパッケージをインストール
1.  動線計測パッケージに含まれるアプリケーションを実行
1.  スクリプト実行


## **手順**
### 1. MQTTブローカーの用意
---
AmazonMQなどフルマネージドのものやMosquitoで自分で構築するなど任意のMQTTブローカーを用意する

<br/>


### 2. Windows端末のセットアップ
---
1. SDKのインストール
    1.  [ダウンロードページ](https://hlds.co.jp/product/tofsdk)より、Windows用の最新のSDKをダウンロードする（例: HldsTofSdk.2.3.0vs2015.zip）<br/> ※ Google Chromeだとダウンロードできない場合があるためその際はブラウザを変更する
    1.  zipファイルを展開し、ドライバのインストーラを実行する　
    <br/> 例 ``HldsTofSdk.2.3.0vs2015\x64\tofdriver\tof_driver_x64_v2.3.0_Installer``

    ※ インストーラ実行時にエラーが発生した場合は同封されているマニュアルで対応方法を確認する
    ``HldsTofSdk.2.3.0vs2015\manual``
1. 動線計測パッケージのダウンロード
    1.  [ダウンロードページ](https://hlds.co.jp/product/tofsdk/peopletrack)より、最新版をダウンロードする（例: PeopleTracking_v200.zip）
    2. 任意の場所でzipファイルを展開する

<br/>

### 3. LiDARセンサーの設定変更
---
1. IPアドレスの変更
    1.  ``http://<LiDARセンサーのIPアドレス>``をブラウザで開きコンソール画面にアクセスする
        1.  初期IP: ``192.168.0.105``、初期パスワード: ``admin``
    1.  ネットワーク設定メニューを開きWindows端末と同一のネットワークとなるようにIPアドレスを変更する
        1. 併せてMACアドレスをコピーしておく

<br/>


### 4. HumanCounterPro（動線計測アプリケーション）の実行
---
HumanCounterProの設定は``PeopleTracking_v200\PeopleTracking``に存在するXMLファイル（``Store*.xml、HumanCounterPro.xml``）に記載されており、これらのXMLファイルはアプリケーション起動時に読み込まれるため、これらのXMLファイルを修正することで任意の設定を行うことができる。
今回の手順で修正するのは、必須である``StoreTof.xml``と``HumanCounterPro.xml``（単にHumanCounterPro.exeを動かすだけであれば不要、ソケット通信する場合必要）。

<br/>

1. ``StoreTof.xml``にLiDARセンサーのIPアドレスとMACアドレスを設定
```xml:StoreTof.xml
- 略 -
    <Tof>
        <PcNo>1</PcNo>
        <TofNo>1</TofNo>
        <Mac>LiDARセンサーのMACアドレス</Mac>　← 修正する
        <Ip>LiDARセンサーのIPアドレス</Ip>　← 修正する
        <Height>2260</Height>
        <AngleX>72</AngleX>
        <AngleY>0</AngleY>
        <AngleZ>87</AngleZ>
        <Direction>161</Direction>
        ...
- 略 -
```
2.  ``HumanCounterPro.xml``にて「StoreHuman（動線データ）」、「HumanCount(ラインカウント)」の2種類のデータのソケット出力を有効にする
```xml:HumanCounterPro.xml
- 略 -
    <Output>
        <StoreHuman>
            <Valid>1</Valid> ← 1にする ※0の場合は無効となる
            <Socket>
                <Valid>1</Valid> ← 1にする
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
            <Valid>1</Valid> ← 1にする
            <PeriodSec>60</PeriodSec>
            <Socket>
                <Valid>1</Valid> ← 1にする
                <Ip>127.0.0.1</Ip>
                <Port>6667</Port>
            </Socket>
            <File>
                <Valid>0</Valid>
            </File>
        </HumanCount>
        ...
- 略 -
```

3. 【HumanCount（ラインカウント）を使用する場合にこの手順を実施】``TofStitcher.exe``を使用してラインを引く

     HumanCountはラインを跨いだ人数をカウントしたデータであるため、そもそもラインを設定しておく必要がある。ラインの設定は動線計測パッケージに含まれる``TofStitcher.exe``で行うことができる
     1. ``TofStitcher.exe``を使用してIN用、OUT用のラインを計2つ設定する
        1. ``TofStitcher.exe``の詳しい操作方法は同封されている``HLDS_TOF_TofStitcher_操作マニュアル.pdf``を参照すること
    1.  ``StoreCount.xml``の``<Count>/<CountName>``を編集し、IN用・OUT用それぞれのカウントグループを以下の命名規則に則った名前に修正する
    ```
    IN用： <任意の英数字の名前>_in
    OUT用： <任意の英数字の名前>_out
    ```
    ```xml:StoreCount.xml
    - 略 -
        <!-- 例 IN用 -->
        <Count>
            <CountName>entrance_1_in</CountName> ← 修正する
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
    - 略 -
    ```

1.  ``HumanCounterPro.exe``を実行する
    1. 起動することを確認する

1.  ソケット通信ができるか確認する
    1. ``PeopleTracking_v200\SocketReceiver\ReceiveTest.exe``を実行し、データを受信できるか確認する

<br/>

### 5. MQTTブローカーにセンシング結果を送信する
---
1.  スクリプト一式をWindows端末に配置する
    - ``lidar_position_sensor_observer.py``
    - ``lidar_inout_sensor_observer.py``

1.  スクリプト一式と同じディレクトリに``.env``ファイルを作成し、自分のMQTTブローカーに関する情報を設定する
```.env
MQTT_HOST = 'your-broker.com'
MQTT_TOPIC = '/lidar/position' → lidar_position_sensor_observer.pyを使う場合
# MQTT_TOPIC = '/lidar/inout' → lidar_inout_sensor_observer.pyを使う場合
MQTT_USER = 'your-username'
MQTT_PASSWORD = 'your-password'
```

2.  ``lidar_*_sensor_observer.py``を実行する

>スクリプトを確認し、自身の環境にインストールされていないモジュールがある場合は足りないものをインストールしてください。
```
※ HumanCounterPro.exeが実行中であること

「人の位置」を送信する
$ python lidar_position_sensor_observer.py

「ラインを跨いだ人数のカウント」送信する
$ python lidar_inout_sensor_observer.py
```

**出力の仕様**

- lidar_position_sensor_observer.py

|項目|内容|
|-|-|
|プロトコル|MQTTS|
|頻度| LiDARセンサーの出力頻度設定による |
|フォーマット|JSON |

**出力サンプル**
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

|項目|内容|
|-|-|
|プロトコル|MQTTS|
|頻度| LiDARセンサーの出力頻度設定による |
|フォーマット|JSON |

**出力サンプル**
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
