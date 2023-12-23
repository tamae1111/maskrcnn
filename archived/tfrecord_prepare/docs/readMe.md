# create_tf_recordを実行するための環境構築手順

# 1:protobufのinstall
# 2:pathを通す
# 3:protocmoduleを使用するための前準備として.pyファイルの生成
git clone https://github.com/tensorflow/models.git

cd models/research

brew install protobuf
brew upgrade protobuf
protoc --version

export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim

protoc -I=./ --python_out=./ ./object_detection/protos/*.proto


# ※:もしエラーが出た場合は、破壊的変更の影響の可能性もあるので、以下コマンドを実施して良い
pip install protobuf==3.19.4

pip3 install --upgrade protobuf

pip3 install protobuf==3.20.1

# 4:ファイルの場所に関して
create_tf_record.pyの場所はどこでもいいが、それを呼び出す場所は、パスの関係でmodels/research上で呼び出す必要がある。

# 5:必要ファイルに関して
output_label_map.pbtxtにラベルの種類分記載が必要。
annotations/trainval.txtに対象のファイル名を格納する必要がある。
makeLabelMap.pyとgetTrainval.pyを使用すると楽に作成できる。

# 6:create_tf_record.pyに関して
tensorflow ver2に対応できるように中身を複数箇所変更している。

# 7:tensorRecordの実行コマンド
python3 /Users/tamae/gitdir/maskrcnn/prepare/create_tf_record.py \
    --annotations_dir=/Users/tamae/gitdir/maskrcnn/prepare/annotations \
    --images_dir=/Users/tamae/gitdir/maskrcnn/prepare/images \
    --output_dir=/Users/tamae/gitdir/maskrcnn/data/tf_records \
    --label_map_path=/Users/tamae/gitdir/maskrcnn/prepare/output_label_map.pbtxt


※以下のようにpwdを引数に入れるのもあり`pwd`/annotations \

# version
protoc --version                                     
libprotoc 3.21.12

python3 -c 'import tensorflow as tf; print(tf.__version__)'
2.11.0

python3 -V 
Python 3.10.10

# コマンド実行パス
/Users/tamae/gitdir/machinL/models/research

# 対象ファイル設置パス
build-segmentation
├── tfRecord
│   ├── annotations
│   │   ├── 20MP_20221201121542.xml
│   │   └── trainval.txt
│   ├── create_tf_record.py



# 現状バグる問題点考察
# create_tf_record.pyが怪しい可能性がある。
annotationのラベルの場所が設定されているのが怪しそう。
でもなんかうまいこと行ってた気もするのが少しあれだが。
↓
多分怪しくなかった

次の容疑者は以下、
image/object/is_crowd", "image/object/mask 、"image/object/area "がないので、これを固定値で入れるように回収するのもありかも
bytes_list {
value: "0"
}
