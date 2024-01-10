import torch

from modules.MLparamaters import getMLParamaters

from modules.fasterRcnn import model_custom,customDataloader
import numpy as np
from modules.smallTask import printFileCount,printTree,printIsAvailableTorchCuda
 
paramaters = getMLParamaters()

# トレーニング実行の処理
def train():
    printIsAvailableTorchCuda()

    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu') 

    two_dir=[paramaters.bdd_xml,paramaters.bdd_img]

    printTree("/opt/ml")
    printFileCount(paramaters.bdd_xml)
    printFileCount(paramaters.bdd_img)


    train_dataloader = customDataloader(two_dir,paramaters.dataset_class,paramaters.batch_size,paramaters.scale)
    

    # ここ運ゲーでバグることがあるが、def model_custom ():のコードを実行などして再実行すると通ることがある。
    # もしかしたら名前が悪いかもしれないので変えたら治るかも　
    # 該当のバグ forward() missing 1 required positional argument: 'images'
    model_c = model_custom(paramaters.dataset_class)
    params = [p for p in model_c.parameters() if p.requires_grad]

    # stable ver
    optimizer = torch.optim.SGD(params, lr=0.005, momentum=0.9, weight_decay=0.0005)

    # try ver ↓ 現状SGDの方がいいので、一旦コメントアウト
    # optimizer = torch.optim.Adam(params, lr=0.005, betas=(0.9, 0.999), eps=1e-08, weight_decay=0.0005, amsgrad=False)

    num_epochs = paramaters.epochs

    model_c.cuda()

    model_c.train()#学習モードに移行

    loss_list=[]

    print("train_dataloader is\n",train_dataloader)
    for epoch in range(num_epochs):
        loss_epo=[]
    
        # model_c.train()#これから学習開始
        for i, batch in enumerate(train_dataloader):
    
            images, targets,_ = batch #####　batchはそのミニバッジのimage、tagets,image_idsが入ってる
            
            images = list(image.to(device) for image in images)
            targets = [{k: v.to(device) for k, v in t.items()} for t in targets]
            
            ##学習モードでは画像とターゲット（ground-truth）を入力する
            ##返り値はdict[tensor]でlossが入ってる。（RPNとRCNN両方のloss）
            loss_dict= model_c(images, targets)
            losses = sum(loss for loss in loss_dict.values())
            loss_value = losses.item()
            
            optimizer.zero_grad()
            losses.backward()
            optimizer.step()

            #lossの保存
            loss_epo.append(loss_value)
    
            if (i+1) % 10== 0:
                print(f"epoch #{epoch+1} Iteration #{i+1} loss: {loss_value}") 
            
        #Epochごとのlossの保存
        loss_list.append(np.mean(loss_epo))
        torch.save(model_c, paramaters.model_path)
    
