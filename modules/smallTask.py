import os
import pathlib
import glob
import torch




def printFileCount(dir):
    initial_count = 0
    print("in printFileCount")
    for path in os.listdir(dir):
        if os.path.isfile(os.path.join(dir, path)):
            initial_count += 1
    print("file count is",initial_count)
    print("in dir ",dir)

def printTree(path, layer=0, is_last=False, indent_current='　'):
    print("printTree start")
    if not pathlib.Path(path).is_absolute():
        path = str(pathlib.Path(path).resolve())

    # カレントディレクトリの表示
    current = path.split('/')[::-1][0]
    if layer == 0:
        print('<'+current+'>')
    else:
        branch = '└' if is_last else '├'
        print('{indent}{branch}<{dirname}>'.format(indent=indent_current, branch=branch, dirname=current))

    # 下の階層のパスを取得
    paths = [p for p in glob.glob(path+'/*') if os.path.isdir(p) or os.path.isfile(p)]
    def is_last_path(i):
        return i == len(paths)-1

    # 再帰的に表示
    for i, p in enumerate(paths):

        indent_lower = indent_current
        if layer != 0:
            indent_lower += '　　' if is_last else '│　'

        if os.path.isfile(p):
            branch = '└' if is_last_path(i) else '├'
            print('{indent}{branch}{filename}'.format(indent=indent_lower, branch=branch, filename=p.split('/')[::-1][0]))
        if os.path.isdir(p):
            printTree(p, layer=layer+1, is_last=is_last_path(i), indent_current=indent_lower)

def printTorchVersions():
    import torchaudio
    import torchvision
    import torchtext

    print("printTorchVersions start")
    print(torch.__version__)
    print(torchaudio.__version__)
    print(torchvision.__version__)
    print(torchtext.__version__)

    print("torch.cuda.is_available()",torch.cuda.is_available())
    print("torch.version.cuda",torch.version.cuda)
    print("torch.cuda.device_count()",torch.cuda.device_count())
    print("torch.cuda.get_device_capability()",torch.cuda.get_device_capability())
    print("torch.cuda.get_device_name()",torch.cuda.get_device_name())
    print("torch.backends.cudnn.is_available()",torch.backends.cudnn.is_available())

    print("torch.backends.cudnn.version()",torch.backends.cudnn.version())

def printIsAvailableTorchCuda():
    '''
    cudaが有効かのprint
    nvidiaドライバー、cuda、torchで相互に有効なバージョンを使用する必要がある
    '''
    print("torch.cuda.is_available() is \n",torch.cuda.is_available())

if __name__ == '__main__':
    dir = "./"
    printIsAvailableTorchCuda()