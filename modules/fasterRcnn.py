import torch
from torchvision import transforms

import torchvision
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision.models.detection import FasterRCNN_ResNet50_FPN_V2_Weights
 
from PIL import Image
from glob import glob
import xml.etree.ElementTree as ET 


# @profile
class MyDataset(torch.utils.data.Dataset):
    
        def __init__(self,image_dir,xml_dir,scale,classes):
            
            super().__init__()
            self.image_dir = image_dir
            self.xml_dir = xml_dir
            self.image_ids = sorted(glob('{}/*'.format(xml_dir)))
            self.scale=scale
            self.classes=classes
            
        def __getitem__(self, index):
    
            # 入力画像の読み込み
            image_id=self.image_ids[index].split("/")[-1].split(".")[0]
            
            # MEMO:ここで、特定のimageのみに絞っているので、メモリの無駄遣いは多くないと思われる
            image = Image.open(f"{self.image_dir}/{image_id}.jpg")
            
            #画像のスケール変換
            t_scale_tate=self.scale ##目標のスケール(縦)
            #縮小比を計算
            ratio=t_scale_tate/image.size[1]
            #目標横スケールを計算
            t_scale_yoko=image.size[0]*ratio
            t_scale_yoko=int(t_scale_yoko)
            
            #print('縮小前:',image.size)
            #print('縮小率:',ratio)
            #リサイズ
            image = image.resize((t_scale_yoko,t_scale_tate))
            #print('縮小後:',image.size)
  
            # ここがデータ拡張を行う箇所
            transform = transforms.Compose([transforms.ToTensor()])
            image = transform(image)
        
            transform_anno = xml2list(self.classes)
            path_xml=f'{self.xml_dir}/{image_id}.xml'
            
            annotations,obje_num= transform_anno(path_xml)

            boxes = torch.as_tensor(annotations['bboxes'], dtype=torch.int64)
            labels = torch.as_tensor(annotations['labels'], dtype=torch.int64)

            #bboxの縮小
            #print('縮小前:',boxes)
            boxes=boxes*ratio

            # boxesのshapeが空になってる際のエラー表示処理
            if boxes.numel() == 0:
                
                print("check file, torch size is zero")
                print("path_xml",path_xml)
                print('boxes.shape:',boxes.shape)
                print('boxes.numel():',boxes.numel())
                print('type(boxes.shape):',type(boxes.shape))
            # ここまで boxesのshapeが空になってる際のエラー表示処理

            area = (boxes[:, 3]-boxes[:, 1]) * (boxes[:, 2]-boxes[:, 0])
            area = torch.as_tensor(area, dtype=torch.float32)

            iscrowd = torch.zeros((obje_num,), dtype=torch.int64)

            target = {}
            target["boxes"] = boxes
            target["labels"] = labels+1
            target["image_id"] = torch.tensor([index])
            target["area"] = area
            target["iscrowd"] = iscrowd
            return image, target,image_id
        
        def __len__(self):

            return len(self.image_ids)
        
# two_dirには全img、xmlパスが格納されている
def customDataloader (two_dir,dataset_class,batch_size,scale=720):
    xml_dir=two_dir[0]
    image_dir=two_dir[1]
    dataset = MyDataset(image_dir,xml_dir,scale,dataset_class)

    #データのロード
    torch.manual_seed(2020)
    
    def collate_fn(batch):
        return tuple(zip(*batch))

    custom_dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True,collate_fn=collate_fn)
    
    return custom_dataloader

def model_custom (dataset_class):
    #モデルの定義
    
    # new ※weights="default"でも良さそうではあった
    weights = FasterRCNN_ResNet50_FPN_V2_Weights.DEFAULT
    model = torchvision.models.detection.fasterrcnn_resnet50_fpn_v2(weights=weights)
    
    num_classes=len(dataset_class)+1
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)
    return model


class xml2list(object):
    
    def __init__(self, classes):
        self.classes = classes
    
    # 格納した変数呼び出し時にパスからアノテーションデータが読み込まれる
    def __call__(self, xml_path):
        
        xml = ET.parse(xml_path).getroot() # ET = ElementTree
        
        boxes = []
        labels = []
        zz=0 # iterator
        
        for zz,obj in enumerate(xml.iter('object')): # xml内のobjectをデータ化したもの
            
            label = obj.find('name').text
          
            ##指定クラスのみ

            if label in self.classes :
                bndbox = obj.find('bndbox')
                xmin = int(bndbox.find('xmin').text)
                ymin = int(bndbox.find('ymin').text)
                xmax = int(bndbox.find('xmax').text)
                ymax = int(bndbox.find('ymax').text)
                boxes.append([xmin, ymin, xmax, ymax])
                labels.append(self.classes.index(label))
            else:
                continue
            
        num_objs = zz + 1

        anno = {'bboxes':boxes, 'labels':labels}

        return anno,num_objs
    