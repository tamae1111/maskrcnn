

## pathName = "/Users/tamae/gitdir/maskrcnn/custombdd/img"


import os
from zipfile import ZipFile

def zip_images(folder_path, zip_filename):
    # フォルダ内の画像ファイルを取得
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    # Zipファイルを作成して画像ファイルを追加
    with ZipFile(zip_filename, 'w') as zip_file:
        for image_file in image_files:
            image_path = os.path.join(folder_path, image_file)
            zip_file.write(image_path, image_file)

    print(f'画像ファイルを"{zip_filename}"に圧縮しました。')

# フォルダのパスとZipファイル名を指定して呼び出し
# folder_path = '/Users/tamae/gitdir/maskrcnn/custombdd/img'
# zip_filename = 'images.zip'
# zip_images(folder_path, zip_filename)


def zip_xmls(folder_path, zip_filename):
    # フォルダ内の画像ファイルを取得
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.xml'))]

    # Zipファイルを作成して画像ファイルを追加
    with ZipFile(zip_filename, 'w') as zip_file:
        for image_file in image_files:
            image_path = os.path.join(folder_path, image_file)
            zip_file.write(image_path, image_file)

    print(f'画像ファイルを"{zip_filename}"に圧縮しました。')

folder_path = '/home/ec2-user/SageMaker/fasterRcnn/colab_frcnn/custombdd//xml'
zip_filename = 'xmls.zip'
zip_xmls(folder_path, zip_filename)