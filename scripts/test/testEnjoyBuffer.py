"""
調査メモ1

encoder処理とデコーダー処理解析メモ

## encoder処理メモ

    # いちいちファイル入出力すると時間も制御もめんどいのでメモリを活用するためにBytesIOを使用。
    buffer = BytesIO() # メモリの格納先を確保

    np.save(buffer, array_like) # メモリへ受け取ったobjを保存

    return buffer.getvalue() # buffereの中身を取得し返却

## decoder処理メモ
    
    stream = BytesIO(npy_array) # 受け取ったnpy_arrayをBytesIOに変換
    return np.load(stream, allow_pickle=True) # numpy_array型で読み取り返却する

実際の画像分析処理ではcontent_typeが何か確認する 
 → 結果 画像をreadしたものを渡す場合はinput_fnを改造する必要がある。
 → requestBodyはstringのため、以下のようにnp.frombuffer(request_body, dtype='uint8'

 
default_output_fnの想定インプット形式

"""

"""
import sagemaker.serializers as sl
sl.IdentitySerializer

調査メモ2
以下調査をしたところ、IdentitySerializerは何もせずに渡すものと判明



sagemaker.serializers.IdentitySerializer("image/jpeg")
 → 
"""

"""
調査メモ3
結論、この記事の
https://dev.classmethod.jp/articles/realtime-inference-on-sagemaker-using-by-pose-estimation-model-pytorch-own-algorhythm/

input_fn、model_fnを参考にほぼコピペで要素だけ入れ替えてあげれば割とサクッと作れる
①input_fnはコピペ。

②model_fnの中身は以下。
use_model=torch.load(paramaters.path+'/models/model.pt')
return use_model

③predict_fn の中身も引数のmodelでmakeInferenceImageを使うように書き換えてあげればoK
まあmakeInferenceImageよりもgetInferenceImageを新しく作って、それを呼び出してreturnする形に変えてあげる
"""



import matplotlib.pyplot as plt
import numpy as np
import cv2 


# 型確認のための汎用メソッド
def showDetail(obj,name):
    obj_type = type(obj)
    print(f"type({name})",obj_type) 
    if obj_type == np.ndarray:
        print(f"{name}.shape",obj.shape) 
    
filename = 'images/testImage.jpg'

# Read image into memory
payload = None
with open(filename, 'rb') as f:
    payload = f.read()
showDetail(payload,"payload") # type(payload) <class 'bytes'>

frombuff = np.frombuffer(payload, dtype='uint8') # byteをnumpyにしている(1次元)
showDetail(frombuff,"frombuff") # frombuff.shape (3002800,)

input_data = cv2.imdecode(frombuff, cv2.IMREAD_UNCHANGED) # numpyを画像の形式にdecodeしている。
showDetail(input_data,"input_data") # input_data.shape (2565, 3500, 3)

bytearray_data = bytearray(payload)
showDetail(bytearray_data,"bytearray_data") # input_data.shape (2565, 3500, 3)

# plt.imshow(input_data) 
plt.show()



