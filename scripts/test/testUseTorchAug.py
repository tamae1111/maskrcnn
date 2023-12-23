import torch
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import numpy as np
import cv2

# OpenCVを使って画像を読み込む
filename = 'images/testImage.jpg'

img = cv2.imread(filename)
#BGRをRGBに変換
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

print("type(img_rgb)")
print(type(img_rgb)) # <class 'numpy.ndarray'>

#データに加える変換を定義
transform = transforms.Compose([
    transforms.ToPILImage(),#　これがないと以下エラーとなる　TypeError: img should be PIL Image. Got <class 'numpy.ndarray'>
    transforms.ColorJitter(brightness=0.3, contrast=0.5) #今回は明るさ、コントラストを変更
])

trans_img = transform(img_rgb)

#画像描画用の関数
def visualize(original, augmented):
  fig = plt.figure()
  plt.subplot(1,2,1)
  plt.title('Original image')
  plt.imshow(original)

  plt.subplot(1,2,2)
  plt.title('Augmented image')
  plt.imshow(augmented)

visualize(img_rgb, trans_img)

plt.show()