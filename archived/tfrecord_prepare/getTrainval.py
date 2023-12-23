import os

def printFileList(path):
    ###  特定のディレクトリ配下のファイル名のみ取得
    fileList = [os.path.splitext(os.path.basename(f))[0] for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    for f in fileList:
        print(f)

if __name__ == '__main__':
    path = "./scripts/tfRecord/images"
    printFileList(path)