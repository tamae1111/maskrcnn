FROM ubuntu:latest


# timezone setting
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt update
RUN apt install -y libopencv-dev

ENV TZ=Asia/Tokyo

# これいるかあやしいけど、ひとまず残しておく
ENV PATH="/opt/program:${PATH}"

RUN apt-get install tzdata libturbojpeg python3-tk python3-pip libsm6 libxrender1 libxext-dev -y

RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools
RUN pip3 install sagemaker-training

# pytorchをインストール
RUN pip3 install torch==2.1.2 torchvision==0.16.2 torchaudio==2.1.2 -f https://download.pytorch.org/whl/torch_stable.html
RUN pip3 install opencv-python
RUN pip3 install matplotlib

# Pipfileなどをコンテナ内にコピー
COPY . /opt/ml/code

# 作業ディレクトリを設定
WORKDIR /opt/ml/code

# trainファイルに実行権限を付与するが、今んとこ不要なのでコメントアウト
# RUN chmod +x /opt/ml/code/train.py

ENV SAGEMAKER_PROGRAM sagemaker_entry_point.py