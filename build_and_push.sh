%%sh

# アルゴリズム名
algorithm_name=hoge

# アカウントIDを取得する
account=$(aws sts get-caller-identity --query Account --output text)

# リージョンを取得する。リージョンが取得できなければ、us-west-2とする
region=$(aws configure get region)
region=${region:-us-west-2}

# コンテナイメージを保存する、ECRのリポジトリ名
fullname="${account}.dkr.ecr.${region}.amazonaws.com/${algorithm_name}:latest"

# リポジトリが存在しない場合には新たに作成する
aws ecr describe-repositories --repository-names "${algorithm_name}" > /dev/null 2>&1

if [ $? -ne 0 ]
then
    aws ecr create-repository --repository-name "${algorithm_name}" > /dev/null
fi

# DockerでECRへログインするためのコマンドを取得し、そのまま実行する
$(aws ecr get-login --region ${region} --no-include-email)


# 学習/推論用コンテナイメージを作成(ビルド)する
docker build  -t ${algorithm_name} .

# 作成したコンテナイメージにECR用のタグを設定する
docker tag ${algorithm_name} ${fullname}

# ECRのリポジトリへコンテナイメージをプッシュ(保存)する
docker push ${fullname}