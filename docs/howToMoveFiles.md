# howToMoveFiles.py用途
1 訓練データの移動

2 tf-recordについては現状結局使っていないので、新しく作る参考程度に見るのが良い

# 訓練データ作成手順書
基本使用するのは以下のファイル
/Users/tamae/gitdir/maskrcnn/scripts/moveTrainData.py

上記のテストコードの中身にパスを記載するなどして自由に操作するのも良い。
test_moveTrainData.pyを見て、使用イメージを掴む

基本以下の2コマンドで動くように修正し実行するだけ
test.test_deleteXMLSubObjects()
test.test_moveXMLFiles()
