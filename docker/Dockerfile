FROM ubuntu:latest


# timezone setting
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update &amp;amp;amp;amp;&amp;amp;amp;amp; apt-get install -y tzdata
RUN apt update
RUN apt install -y libopencv-dev

ENV TZ=Asia/Tokyo
ENV PATH="/opt/program:${PATH}"




RUN chmod +x /opt/ml/code/train.py # trainファイルに実行権限を付与する

WORKDIR /opt/ml/code

RUN apt-get install libturbojpeg python3-tk python3-pip libsm6 libxrender1 libxext-dev -y
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools

RUN pip3 install sagemaker-training
RUN pip3 install -r /opt/init/requirements.txt
RUN pip3 install -r /opt/init/requirements2.txt

RUN pip3 install opencv-python

# Pipfileなどをコンテナ内にコピー
COPY . /

# COPY program /opt/ml/code
# COPY init /opt/init

# pipenvを使ってPipfileに書いてあるライブラリをインストール
RUN pipenv install --skip-lock

# pytorchをインストール
RUN pip3 install torch==2.0.1+cpu torchvision==torchvision==0.16.2+cpu torchaudio==0.9.1 -f https://download.pytorch.org/whl/torch_stable.html


ENV SAGEMAKER_PROGRAM /opt/ml/code/train.py