import torch
import torchvision
from glob import glob

import cv2
import glob
import matplotlib.pyplot as plt
import copy
from modules.MLparamaters import getMLParamaters
import numpy as np
import logging
import sys

# logger設定
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

# 他パラメータ設定
paramaters = getMLParamaters()
colors = paramaters.colors
data_class=copy.copy(paramaters.dataset_class)
data_class.insert(0, "__background__")
classes = tuple(data_class)

# detection box　を図字するメソッド
def testShowInferenceImage(use_model):
    logger.info('START testShowInferenceImage')
    logger.info(f'type: {type(use_model)}')
    use_model.to(paramaters.divice)
    use_model.eval() # dropoutやbatch normの on/off
    
    for imgfile in sorted(glob.glob(paramaters.test_path+'/*')): # テストフォルダにある画像分ループ実行

        img = cv2.imread(imgfile)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = getProcessedImage(img,use_model)
        plt.figure(figsize=(15,10))
        plt.imshow(img)

    plt.show()


def getProcessedImage(img:np.ndarray,use_model):
    logger.info('START getProcessedImage')
    logger.info(f'type: {type(img)}')
    logger.info(f'type: {type(use_model)}')
    
    # tensor型への変換
    image_tensor = torchvision.transforms.functional.to_tensor(img)

    with torch.no_grad():
        prediction = use_model([image_tensor.to(paramaters.divice)]) # ここで予測結果がpredictionに格納される

    img = getLabelAddedImage(img,prediction[0])

    return img


def getLabelAddedImage(img,prediction_first):
    logger.info('START getLabelAddedImage')
    logger.info(f'type: {type(img)}')
    logger.info(f'type: {type(prediction_first)}')
    for i,box in enumerate(prediction_first['boxes']): # 以降1イメージ内の予測されたラベル数分ループ処理
        score = prediction_first['scores'][i].cpu().numpy()
        if score > 0.5:
            # 個数を抽出したいときはこの中に処理を追記すればよい
            score = round(float(score),2)

            # category(cat) 1,2など、何番目のcategoryかの情報
            cat = prediction_first['labels'][i].cpu().numpy()

            txt = '{} {}'.format(classes[int(cat)], str(score))
            font = cv2.FONT_HERSHEY_SIMPLEX

            # 文字列の幅の表示の幅と高さ取得
            cat_size = cv2.getTextSize(txt, font, 0.5, 2)[0]

            c = colors[int(cat)]
            box=box.cpu().numpy().astype('int')

            # 四角描画
            cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), c , 2)

            # テキストの周りの小さな四角描画
            cv2.rectangle(img,(box[0], box[1] - cat_size[1] - 2),(box[0] + cat_size[0], box[1] - 2), c, -1)

            # テキスト描画
            cv2.putText(img, txt, (box[0], box[1] - 2), font, 0.5, (0, 0, 0), thickness=1, lineType=cv2.LINE_AA)

    return img
    


# 特定のラベルのカウント数を画像に添付して表示するメソッド
def makeAddedSpecificCount(use_model):
    use_model.to(paramaters.divice)
    use_model.eval() # dropoutやbatch normの on/off
    default_x_position = 50
    
    for imgfile in sorted(glob.glob(paramaters.test_path+'/*')):# imgfile = 1ファイル
        
        countList = [0 for x in data_class]

        img = cv2.imread(imgfile)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # tensor型への変換
        image_tensor = torchvision.transforms.functional.to_tensor(img)

        with torch.no_grad():
            prediction = use_model([image_tensor.to(paramaters.divice)]) # ここで予測結果がpredictionに格納される

        for i,box in enumerate(prediction[0]['boxes']): # 以降1イメージ内の検出されたラベル数分ループ処理
            score = prediction[0]['scores'][i].cpu().numpy()
            if score > 0.5:
                cat = prediction[0]['labels'][i].cpu().numpy()
                countList[int(cat)] += 1
                
        print("countList is",countList)
        
        showPositionIndex = 0
        for i, count in enumerate(countList):
            if i == 0 or count == 0: # backgroundはスキップ
                continue
                
            showPositionIndex += 1
                
            showPosition = showPositionIndex * 15
            
            font = cv2.FONT_HERSHEY_SIMPLEX
            txt = 'label:{},count:{}'.format(classes[i],str(count))

            # 文字列の幅の表示の幅と高さ取得
            cat_size = cv2.getTextSize(txt, font, 0.5, 2)[0]
            
            c = colors[i]
            
            # countListの四角描画
            cv2.rectangle(img,(default_x_position, showPosition),(default_x_position + cat_size[0], cat_size[1] + showPosition), c, -1)

            # countListのテキスト描画
            cv2.putText(img, txt, (default_x_position, cat_size[1] + showPosition), font, 0.5, (0, 0, 0), thickness=1, lineType=cv2.LINE_AA)

        plt.figure(figsize=(15,10))
        plt.imshow(img)
    plt.show()