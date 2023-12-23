import matplotlib.pyplot as plt
from PIL import Image
import io 

filename = 'images/testImage.jpg'

# Read image into memory
payload = None
with open(filename, 'rb') as f:
    payload = f.read()

print("payload is")
print(type(payload)) # <class 'bytes'>
print(payload[:100]) # b'\xff\xd8\xff\xe1\x02〜〜〜〜

testBody=bytearray(payload)

print("testBody is")
print(type(testBody)) # <class 'bytearray'>
print(testBody[:100]) # bytearray(b'\xff\xd8\xff\xe1\x02〜〜〜〜

img_bin = io.BytesIO(payload)
print("img_bin is")
print(img_bin) # メモリ格納先が表示される　<_io.BytesIO object at 0x10d68d760>
print(type(img_bin)) # <class '_io.BytesIO'>
# print(img_bin[:100]) _io.BytesIO' object is not subscriptable
img = Image.open(img_bin)
plt.imshow(img)
img.save("testOutPut.png","PNG") # 問題なく表示される
