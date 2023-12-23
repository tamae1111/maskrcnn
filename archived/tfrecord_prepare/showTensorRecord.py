from __future__ import absolute_import, division, print_function, unicode_literals
import tensorflow as tf
import numpy as np
import IPython.display as display

# TFRecordのパスを指定する

def showTfRecord(filesName):
    # 変数定義
    raw_dataset = tf.data.TFRecordDataset(filesName)

    # 読み込んだ内容を別の形式に書き出す
    # （.txtでも良い。jsonだとエディタ次第だが色ついて見やすくなるのでtxtよりオススメ）
    tfr_data = 'tfr.json'

    for raw_record in raw_dataset.take(1):
        example = tf.train.Example()
        example.ParseFromString(raw_record.numpy())
        print(example)

        # ファイルに書き出す。書き出さなくてもコンソールで見れるので必須ではない。
        with open(tfr_data, 'w') as f:
            print(example, file=f)


def convertPascal2TfRecord():
    print()
    #!python3 object_detection/dataset_tools/create_pascal_tf_record.py --data_dir=<path_to_pascal_voc_dataset> --year=<pascal_voc_dataset_year> --output_path=<path_to_output_tfrecord>
    # python3 object_detection/dataset_tools/create_pascal_tf_record.py --data_dir="/Users/tamae/gitdir/build-segmentation/images/detectAddLabel" --year=2012 --output_path="/Users/tamae/gitdir/build-segmentation/images/detectAddLabel"


if __name__ == '__main__':
    # check
    cocofilesName = 'images/work/tfrecord/coco-train.tfrecord-00000-of-00256'

    createdfilesName = '/Users/tamae/gitdir/maskrcnn/data/tf_records/output_train.record'

    car_defect_Name = '/Users/tamae/gitdir/maskrcnn/data/tf_records/train.record'
    showTfRecord(createdfilesName)