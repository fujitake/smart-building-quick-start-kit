[English](./README.en.md)

# 7セグメントメーターリーダー

7セグメントメーターの値を読み取り、MQTTブローカーに読み取った値を送信する手順です。

## 仕様

### セグメントメーターの読み取り

セグメントメーターの読み取りは [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) を用いて実現しています。
利用方法は [PaddleOCR Quick Start](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.3/doc/doc_en/quickstart_en.md#22-use-by-code) を参考にしています。

PaddleOCR がどのように画像中の文字列を検出しているかは、以下デモページにて確認することができます。適宜ご利用ください。

[https://huggingface.co/spaces/akhaliq/PaddleOCR](https://huggingface.co/spaces/akhaliq/PaddleOCR)

## セットアップ

### 必要なもの

- 検出対象にする7セグメントメーター
> 本手順で使用するスクリプトは、サンプル画像でも動作させることができます。サンプル画像を使う処理はコメントアウトされておりますので、必要な場合は該当箇所のコメントを解除してください。

- カメラ付きPC ※ 本手順の検証では MacBook Pro(2018)を使用しています

>PaddlePaddleモジュールは現在Arm64に対応していないため（2021/10/18時点）、Apple M1が搭載されているMacでは動作しません。

- 本ディレクトリ一式

### 手順

1. OpenCV インストール
   MacOS では、以下のコマンドでインストールします。

```sh
$ brew install opencv
```

2. segment_meter_reader.py と同じディレクトリに`requirements.txt` ファイルを設置し、アプリケーションに必要な Python モジュールをインストールします

```
$ pip3 install -r requirements.txt
```

> Python 3.9.x系の場合、PaddleOCRのインストールが失敗することがあります。その場合は3.8.x系に切り替えてください。

3. 秘匿情報等は環境変数としてスクリプトへ読み込みます  
   `.env.sample` ファイルをコピーして `.env` ファイルを作成し、ファイル内の説明に沿った値を設定してください

## セグメントメーターの数値検出

`segment_meter_reader.py`を実行して、セグメントメーターの値を読み取り、VANTIQ にデータを送信します。

```sh
$ python3 segment_meter_reader.py

```

## 送信詳細

| 項目         | 内容                  |
| ------------ | --------------------- |
| プロトコル   | MQTTS                 |
| 頻度         | 30 秒ごとに 1 回送信  |
| フォーマット | JSON                  |

```
{
  "sensor_id": "string",
  "sensing_value": "string",
  "timestamp": int
}
```

## 注意点

- サンプル画像を基にセグメントメーターの値を検出を確認しました。自身で撮影した画像を利用する場合、正しくセグメントメーターの値を検出できない場合があります。下記注意点を参考にご用意ください。
  - 対象となるメーター 1 つのみを大きく映さないと、正しくメーターの数字を検出することができません。
  - カメラから 0.5m ほどの距離を保ってください。
  - MQTT Broker との通信経路の暗号化・認証は簡易的なものなので、実際の案件で求められるセキュリティレベルに応じて対策ください。
