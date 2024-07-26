# DMM_PURCHASELIST

## 概要

DMMの同人購入リストを取得するためのスクリプトです。  
メールアドレス、パスワードを入れて使用します。  
おそらく、二段階認証が有効な場合は使えないと思います。

## 使い方

1. `pip install selenium` でseleniumをインストールします。
1. `email` `password` を設定します。
1. `python dmm_purchaselist.py` を実行します。
1. `DMM_{today}_PURCHASED_LIST.csv` が生成されます。  
おわり。

## 出力結果

```csv
タイトル,サークル,ジャンル
タイトル,サークル,ジャンル
タイトル,サークル,ジャンル
タイトル,サークル,ジャンル
```
