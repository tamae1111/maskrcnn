import unittest
import numpy as np
import moveTrainData as moveTrain


class moveTrain_Test(unittest.TestCase):

    def test_deleteYoloSubObjects(self):
        path = "/Users/tamae/Library/CloudStorage/GoogleDrive-tamae@iret.co.jp/マイドライブ/MachineL/yolo/yolov7/data/custom_dataset"
        moveTrain.deleteYoloSubObjects(path)

    def test_deleteXMLSubObjects(self):
        path = "/Users/tamae/Library/CloudStorage/GoogleDrive-tamae@iret.co.jp/マイドライブ/MachineL/fasterRcnn/colab_frcnn/custombdd"
        moveTrain.deleteXMLSubObjects(path)

    def test_moveYoloFiles(self):
        inputDir = "/Users/tamae/gitdir/build-segmentation/images/detectAddLabel/1024/"
        outputImgDir = "/Users/tamae/Library/CloudStorage/GoogleDrive-tamae@iret.co.jp/マイドライブ/MachineL/yolo/yolov7/data/custom_dataset/train/images/"
        outputLabelDir = "/Users/tamae/Library/CloudStorage/GoogleDrive-tamae@iret.co.jp/マイドライブ/MachineL/yolo/yolov7/data/custom_dataset/train/labels/"

        moveTrain.moveYoloFiles(inputDir,outputImgDir,outputLabelDir)

    def test_moveXMLFiles(self):
        inputDir = "/Users/tamae/gitdir/build-segmentation/images/detectAddLabel/1024/"
        outputImgDir = "/Users/tamae/gitdir/maskrcnn/custombdd/img/"
        outputLabelDir = "/Users/tamae/gitdir/maskrcnn/custombdd/xml/"

        moveTrain.moveXMLFiles(inputDir,outputImgDir,outputLabelDir)
    

if __name__ == "__main__":
    test = moveTrain()
    test.test_deleteXMLSubObjects()
    test.test_moveXMLFiles()