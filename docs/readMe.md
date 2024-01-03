## 実施時期
2024/01/03


## ディレクトリ構造
maskrcnn
├── Faster_R_CNN_ver_sagemaker.ipynb
└── custombdd 
    ├── img
    ├── test
    └── xml

## 以下使用ディレクトリ解説

### 基本的な実行ファイル(訓練、モデル保存)
maskrcnn
└── Faster_R_CNN_ver_sagemaker.ipynb

### 以下ディレクトリに訓練用のファイル群を格納し、トレーニングを実施する。
maskrcnn
└── custombdd 
    ├── img
    ├── test
    └── xml

## 使用ラベリングツール
labelImg
対象のimg画像を上記imgディレクトリに保存
で生成したアノテーションデータを上記xmlディレクトリに保存


## ラベリング方法
labelImg
対象のimg画像を上記imgディレクトリに保存
で生成したアノテーションデータを上記xmlディレクトリに保存

##　ラベリング前データ作成
作業用のディレクトリに対象のimgファイルを移動する　例：build-segmentation/images/work/input
このとき、変換ごに1024にするため、元々の画像は5472 × 3648が望ましい

build-segmentation/scripts/test/test_shapeChange.py
の
test_trimming43DirectAllを実行して、画像を増加させる。

## トレーニングの実施、検証
Faster_R_CNN_ver_sagemaker_moduled.ipynb
を実行する
※中ではmoudlesのライブラリを読み込み、trainなどを実行



