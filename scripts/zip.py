import shutil

zipName = "zipedFiles"
pathName = "path"

def makeZipFile(zip_name,path):
    shutil.make_archive(zip_name, 'zip', root_dir=path)

if __name__ == "__main__": 
    makeZipFile(zipName,pathName)