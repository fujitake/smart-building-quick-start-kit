[English](./README.en.md)

# 登録者検知

カメラで取得した映像からOpenCVで顔を検出し、あらかじめ登録した顔と一致するかをAWS Rekognitionで判定します。
一致した場合MQTTブローカーに送信します。

## 仕様

### 顔の登録

OpenCV を用いて PC に内蔵されたカメラで、顔写真を 1 枚撮影します。
この顔写真を検出対象とみなし、AWS Rekognition にアップロードします。

アップロードが正しく行えたことを確認するため、アップロード後に同じ写真で顔を照合します。
レスポンスが以下のように Terminal 上に出力されれば成功です。

### 顔の検出

OpenCV を用いて PC に内蔵されたカメラで顔写真を定期的に撮影します。
撮影周期は顔の有無によって変動しますがおよそ 1〜4 秒周期です。

顔が写っている場合、AWS Rekognition で顔を照合し、登録した顔と同じであるかチェックします。
同じ顔であった場合、MQTTブローカーにpublishします。

検出状況に応じて、プログラムを実行した Terminal 上に以下のようなログが出力されます。

```sh
$ python3 person_detect.py
not detected. # 顔が検出されていない
detected.     # 顔を検出した
matched.      # 顔が一致した
```

## セットアップ

### 必要なもの

- カメラ付き PC ※検証では MacBook Pro(2018)を使用

### 手順

1. OpenCV インストール
   MacOS では、以下のコマンドでインストールします。

```sh
$ brew install opencv
```

2. person_detect.py と同じディレクトリに`requirements.txt` ファイルを設置し、アプリケーションに必要な Python モジュールをインストールします

```
$ pip3 install -r requirements.txt
```

3. 秘匿情報等は環境変数としてスクリプトへ読み込みます  
   `.env.sample` ファイルをコピーして `.env` ファイルを作成し、ファイル内の説明に沿った値を設定してください

## 顔の登録

`face_register.py`を実行して、あなたの顔を AWS Rekognition に登録します。

```sh
$ python3 face_register.py

# Activate the camera.
```

本プログラムはレスポンスデータを出力します。  
レスポンスに含まれる FaceId を、VANTIQ のマスターデータに設定してください。

## 顔の検出

`person_detect.py`を実行して、顔を検出し、VANTIQ にデータを送信します。

```sh
$ python3 person_detect.py

# Activate the camera.
```

## 送信詳細

| 項目         | 内容                              |
| ------------ | --------------------------------- |
| プロトコル   | MQTTS                             |
| 頻度         | 新しい顔を検出するごとに 1 回送信 |
| フォーマット | JSON                              |

```JSON
{
  "camera_id": "string",
  "face_id": "string",
  "timestamp": int,
  "similarity": float
}
```

## 注意点

- 本サンプルでは登録・検出できる顔は 1 種類のみです。
- カメラは顔の正面を撮る必要があります。
- カメラから 0.5m ほどの距離を保ってください。
- MQTT Broker との通信経路の暗号化・認証は簡易的なものなので、実際の案件で求められるセキュリティレベルに応じて対策ください。
