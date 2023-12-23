import shutil

zipName = "zipedFile"
pathName = "/Users/tamae/gitdir/maskrcnn/custombdd/img"

# e.g. /home/ec2-user/SageMaker/fasterRcnn/colab_frcnn/custombdd/img

def makeZipFile(zip_name,path):
    shutil.make_archive(zip_name, 'zip', root_dir=path)

if __name__ == "__main__": 
    makeZipFile(zipName,pathName)