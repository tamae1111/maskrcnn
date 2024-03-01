import torch
import os


class paramaterClass:

    #ドットアクセス用の自作クラス
    class DictDotNotation(dict): 
        def __init__(self, *args, **kwargs): 
            super().__init__(*args, **kwargs) 
            self.__dict__ = self 


    result = DictDotNotation()

    # sagemakerの環境変数を支える場合は、s3も使うため、連動してこのフラグをTrueにする
    canUseCUDA:bool =  torch.cuda.is_available()

    useS3:bool = bool(os.environ.get('SM_CHANNEL_TRAINING'))

    # SagemakerAPIで立ち上げたインスタンスの場合
    if useS3:
        # sagemakerの環境変数から取得
        input_data_dir = os.environ.get('SM_CHANNEL_TRAINING')
        bdd_xml= input_data_dir + "/xml"
        bdd_img= input_data_dir + "/img"
        test_path= input_data_dir + "/test"
        model_path = os.environ.get('SM_MODEL_DIR') + "/model.pt"
        # "/opt/ml/model"

    # notebookインスタンスの場合
    elif canUseCUDA:
        basePath = '/home/ec2-user/SageMaker/maskrcnn'
        middle_path = "/custombdd"
        bdd_xml= basePath+ middle_path + "/xml"
        bdd_img= basePath+ middle_path + "/img"
        test_path= basePath+ middle_path + "/test"
        model_path = basePath +'/models/model.pt'
        # CUDAが使えない状態（完全ローカル）

    # 完全ローカルの場合
    else:
        basePath = '/Users/tamae/gitdir/maskrcnn'
        middle_path = "/custombdd"
        bdd_xml= basePath+ middle_path + "/xml"
        bdd_img= basePath+ middle_path + "/img"
        test_path= basePath+ middle_path + "/test"
        model_path = basePath +'/models/model.pt'


    dataset_class = ['person','vehicle','c_vehicle2','c_vehicle3','tank_lorry','truck','c_vehicle','c_vehicle4']
    colors = ((0,0,0),(255,0,0),(0,255,0),(0,0,255),(100,255,100),(100,100,255),(255,255,0),(255,0,255),(0,255,255))

    device = torch.device('cuda') if canUseCUDA else torch.device('cpu') 

    #ハイパーパラメータの指定
    epochs = 5
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
    result["device"] = device
    result["useS3"] = useS3

    print("paramaters are\n",result.items())

def getMLParamaters():
    '''
    return \n
    dict_items([('model_path', '/*****/model.pt'), ('test_path', '/*****/custombdd/test'), ('bdd_img', '/*****/custombdd/img'), ('bdd_xml', '/****/custombdd/xml'), ('dataset_class', ['person', 'vehicle', 'c_vehicle2', 'c_vehicle3', 'tank_lorry', 'truck', 'c_vehicle', 'c_vehicle4']), ('colors', ((0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (100, 255, 100), (100, 100, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255))), ('epochs', 20), ('batch_size', 4), ('scale', 1024), ('device', device(type='cuda')), ('useS3', False)])
    '''

    return paramaterClass.result


if __name__ == '__main__':
    getMLParamaters()