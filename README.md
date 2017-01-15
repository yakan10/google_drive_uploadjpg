# 概要
pythonでGoogle Driveに画像ファイルをアップロードします

# 準備
* Google Accountを作っておく
* Google API コンソールでプロジェクトを新規作成する([Quickstart](https://developers.google.com/drive/v3/web/quickstart/python)を参考に)
* ライブラリのインストール
```
$ pip install --upgrade google-api-python-client 
```

# 実行
認証情報を取得し、同じディレクトリにあるsample.jpgをアップロードします。
```
python google_drive_uploadjpg.py
```

アップロードはRESTのPOSTなので、curl等でも実行できます。
```
sh uploadjpg_curl.sh
```
※事前にスクリプト中のファイルサイズとaccess_tokenを書き換えてください。