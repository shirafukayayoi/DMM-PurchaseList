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

## Googleスプレッドシートにデータを入れてる用も作った

GoogleSheetにデータを入れる用のスクリプトも作りました。  

1. `pip install gspread oauth2client` で必要なライブラリをインストールします。  
1. `credentials.json` を取得して、`dmm_purchaselist.py` と同じディレクトリに配置します。  
1. 追加で`sheet_url`を設定します。
1. `credentials.json` で指定したアカウントにGoogleSheetの編集権限があることを確認します。  
   自分は[https://zenn.dev/yamagishihrd/articles/2022-09_01-google-spreadsheet-with-python](https://zenn.dev/yamagishihrd/articles/2022-09_01-google-spreadsheet-with-python)これを参考にしました。
1. 実行します。

## DIscordのBOTで通知する用も作った

DiscordのBOTで通知する用のスクリプトも作りました。

DiscordのBOTを作成して、トークンを取得します。  
そのトークンを`token`に設定します。
