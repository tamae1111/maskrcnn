from natsort import natsorted
from glob import glob
import os

import shutil

# リファクタ必要
def moveYoloFiles(inputDir,outputImgDir,outputLabelDir):
    # txtファイル関連操作
    extention = ".txt"
    baseNameList = getBaseNameList(inputDir,extention)
    txtList = addExtensionToList(baseNameList,extention)
    for name in txtList:
        shutil.copy2(name, outputLabelDir)

    # txtがあったリストを使ってjpgファイルのコピー操作
    jpgFileList = addExtensionToList(baseNameList,".jpg")
    for name in jpgFileList:
        shutil.copy2(name, outputImgDir)

# リファクタ必要
def moveXMLFiles(inputDir,outputImgDir,outputLabelDir):
    # txtファイル関連操作
    extention = ".xml"
    baseNameList = getBaseNameList(inputDir,extention)
    txtList = addExtensionToList(baseNameList,extention)
    for name in txtList:
        shutil.copy2(name, outputLabelDir)

    # xmlがあったリストを使ってjpgファイルのコピー操作
    jpgFileList = addExtensionToList(baseNameList,".jpg")
    for name in jpgFileList:
        shutil.copy2(name, outputImgDir)
    
def getBaseNameList(path,extention):
    searchDir = os.path.join(path , f"*{extention}")
    originFiles = glob(searchDir)
    deleteName = 'classes.txt'
    originFiles = list(filter(lambda x: not deleteName in x, originFiles))
    res = getBaseFileNameList(originFiles)
    
    return res

def getBaseFileNameList(originFiles:list) -> list:
    originFiles = natsorted(originFiles)
    # 該当するファイルが存在しない場合はassert
    assert len(originFiles) > 0 , 'パスにファイルが存在しません'
    foldar = os.path.dirname(originFiles[0]) # 少しここバグ怖い
    fileList = []
    for fileName in originFiles:
        fileNameBase = os.path.basename(fileName) #e.g. 20MP_20221201143511.txt
        filename_no_extension = os.path.splitext(fileNameBase)[0] # e.g.20MP_20221201143511
        fileList.append(os.path.join(foldar , filename_no_extension))
    res = fileList
    return res

def addExtensionToList(strList:list,extension:str):
    """ e.g. extension ".jpg"
    """
    res = [x + extension for x in strList]
    return res

# 特定のyoloディレクトリ配下のイメージを削除するメソッド
# e.g. path /Users/tamae/Library/CloudStorage/GoogleDrive-tamae@iret.co.jp/マイドライブ/MachineL/yolo/yolov7/data/custom_dataset

def deleteYoloSubObjects(basePath):
    shutil.rmtree(f'{basePath}')
    os.mkdir(f'{basePath}')
    
    # 削除したディレクトリの生成
    def mkdirLocal(path,imagePath,labelPath):
        os.mkdir(f'{path}')
        os.mkdir(f'{path}/{imagePath}/')
        os.mkdir(f'{path}/{labelPath}/')

    imagePath = "images"
    labelPath = "labels"

    middlePath = "test"
    mkdirLocal(f'{basePath}/{middlePath}',imagePath,labelPath)
    middlePath = "train"
    mkdirLocal(f'{basePath}/{middlePath}',imagePath,labelPath)
    middlePath = "valid"
    mkdirLocal(f'{basePath}/{middlePath}',imagePath,labelPath)

def deleteXMLSubObjects(basePath):
    # e.g. basePath /Users/tamae/Library/CloudStorage/GoogleDrive-tamae@iret.co.jp/マイドライブ/MachineL/fasterRcnn/colab_frcnn/custombdd
    shutil.rmtree(f'{basePath}')
    os.mkdir(f'{basePath}')
    
    os.mkdir(f'{basePath}/img')
    os.mkdir(f'{basePath}/test')
    os.mkdir(f'{basePath}/xml')


   
