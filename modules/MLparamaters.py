import torch
import os

def getMLParamaters():
    '''
    return \n
    result["path"]\n
    result["test_path"]\n
    result["bdd_img"]\n
    result["bdd_xml"]\n
    result["dataset_class"]\n
    result["colors"]\n
    result["epochs"]\n
    result["batch_size"]\n
    result["scale"]\n
    result["divice"]\n
    '''

    #ドットアクセス用の自作クラス
    class DictDotNotation(dict): 
        def __init__(self, *args, **kwargs): 
            super().__init__(*args, **kwargs) 
            self.__dict__ = self 


    result = DictDotNotation()


    # sagemakerの環境変数を支える場合は、s3も使うため、連動してこのフラグをTrueにする
    useS3:bool = bool(os.environ.get('SM_CHANNEL_TRAINING'))
    print("useS3 is",useS3)

    if useS3:
        # sagemakerの環境変数から取得
        input_data_dir = os.environ.get('SM_CHANNEL_TRAINING')
        middle_path = "/custombdd"
        bdd_xml= input_data_dir+ middle_path + "/xml"
        bdd_img= input_data_dir+ middle_path + "/img"
        test_path= input_data_dir+ middle_path + "/test"
        model_path = os.environ.get('SM_MODEL_DIR') + "/model.pt"
        # "/opt/ml/model"

    else:
        basePath = '/home/ec2-user/SageMaker/maskrcnn'
        middle_path = "/custombdd"
        bdd_xml= basePath+ middle_path + "/xml"
        bdd_img= basePath+ middle_path + "/img"
        test_path= basePath+ middle_path + "/test"
        model_path = basePath +'/models/model.pt'

    # debug print
    print("input_data_dir is",input_data_dir)
    print("bdd_xml is",bdd_xml)
    print("bdd_img is",bdd_img)
    print("test_path is",test_path)
    print("model_path is",model_path)


    dataset_class = ['person','vehicle','c_vehicle2','c_vehicle3','tank_lorry','truck','c_vehicle','c_vehicle4']
    colors = ((0,0,0),(255,0,0),(0,255,0),(0,0,255),(100,255,100),(100,100,255),(255,255,0),(255,0,255),(0,255,255))

    divice = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu') 

    #ハイパーパラメータの指定
    epochs = 20
    batch_size = 4
    scale = 1024 #画像のスケール設定(縦の大きさを入力)

    result["model_path"] = model_path
    result["test_path"] = test_path
    result["bdd_img"] = bdd_img
    result["bdd_xml"] = bdd_xml
    result["dataset_class"] = dataset_class
    result["colors"] = colors
    result["epochs"] = epochs
    result["batch_size"] = batch_size
    result["scale"] = scale
    result["divice"] = divice
    result["useS3"] = useS3

    return result
