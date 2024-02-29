## build_and_push.shの用途
これはdockerコンテナを作成するためのただの便利スクリプト。
以下のコマンドで代替してもいい。
gitのルートディレクトリから実行する

```
まずは普通にDockerFileを作成し、Dockerにbuildします。
docker build -t test:latest --platform linux/x86_64 .

次にECRのレポジトリを作ります。
aws ecr create-repository --repository-name test --region ap-northeast-1

ecrのget-login-passwordを使ってdockerでログインします。
aws ecr get-login-password | docker login --username AWS --password-stdin 958305726855.dkr.ecr.ap-northeast-1.amazonaws.com/

buildしたimageを使ってECRにtagをつけます。
docker tag test 958305726855.dkr.ecr.ap-northeast-1.amazonaws.com/test:latest

ECRにimageをpushします。
docker push 958305726855.dkr.ecr.ap-northeast-1.amazonaws.com/test:latest
```

できたものをsagemakerのimageタグで使えばいい
多分以下
958305726855.dkr.ecr.ap-northeast-1.amazonaws.com/test:latest


