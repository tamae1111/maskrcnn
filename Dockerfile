FROM ubuntu:latest


# timezone setting
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt update
RUN apt install -y libopencv-dev

ENV TZ=Asia/Tokyo

RUN apt-get install tzdata libturbojpeg python3-tk python3-pip libsm6 libxrender1 libxext-dev -y

RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools

# opencv
RUN pip3 install opencv-python

RUN pip3 install sagemaker-training matplotlib 

# ディレクトリ構造のデバッグのためのinstall
RUN pip3 install pathlib glob2
# pytorchをインストール
RUN pip3 install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 --index-url https://download.pytorch.org/whl/cu118

# Pipfileなどをコンテナ内にコピー
COPY . /opt/ml/code


# SM_NUM_GPUSなどのSageMakerの作成する環境変数を体良く取り込むために、SAGEMAKER_PROGRAMという環境変数を使う
# またこれによってSDK実行時にentrypointの設定を引数でしなくても済むようになる
ENV SAGEMAKER_PROGRAM sagemaker_entry_point.py