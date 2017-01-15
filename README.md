# 概要
pythonでGoogle Driveに画像ファイルをアップロードします
[Quickstart](https://developers.google.com/drive/v3/web/quickstart/python)にしたがって粛々と実装します

# 準備
* Google Accountを作っておく
* Google API コンソールでプロジェクトを新規作成する
1. [Google APIs](https://console.developers.google.com/flows/enableapi?apiid=drive)にアクセス
2. 「プロジェクトを作成」を選択して続行
3. 「APIが有効化されました」->認証情報に進む
4. 「プロジェクトへの認証情報の追加」でキャンセル
5. 「OAuth同意画面」タブ->メールアドレスとユーザーに表示するサービス名を入力して保存
6. 「認証情報」タブ->「認証情報を作成」-> OAuthクライアントID
7. 「その他」を選択して名前に「Drive API Quickstart」と入力->作成
8. OAuthクライアントのダイアログが表示されるがとりあえず「OK」
9. 「OAuth 2.0 クライアント ID」の先ほど作成したIDの横のダウンロードアイコンでファイルをDL
10. DLしたファイルのファイル名を「client_secret.json」にしておく
* ライブラリのインストール
'''
$ pip install --upgrade google-api-python-client 
'''

# 実装
[Quickstartのサンプルコード](https://developers.google.com/drive/v3/web/quickstart/python#step_3_set_up_the_sample)を参考に
jpgをアップロードする部分を追加します

## ソースコード
以下のコードでは、認証情報を取得した後、同じディレクトリにある"sample.jpg"というファイルをアップロードしています

'''google_drive_uploadjpg.py
# -*- coding: utf-8 -*-
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import requests

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# quickstartではhttps://www.googleapis.com/auth/drive.metadata.readonlyだがUpload権限がない
# UploadもできるFullScopeの以下を利用する (UploadだけできるSCOPE探したけど見つからず...)
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
# プロジェクト作成時に入力したアプリケーション名
APPLICATION_NAME = 'Drive API Quickstart'

def get_credentials():
    """
    (quickstart.pyの和訳)
    有効なユーザー認証をストレージ(ローカルに保存された認証情報)から取得する
    なにもローカル保存されてない場合か、保存された認証情報が無効の場合は、
    OAuth2 flowで新しい認証情報を取得する
    
   ・そのまま実行すると自動でブラウザが開いて認証画面に飛ぶ
    ・--noauth_local_webserver オプションをつけるとコンソールにURLが表示される
      表示されたURLをブラウザに入力すると認証画面が表示され、認証後出てきたコードをコンソール上で入力する
    :return: 取得された認証情報
    """

    # ~/.credentials/drive-python-quickstart.jsonに認証情報を保存
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + credential_path)
    return credentials

def upload_jpg(credentials, jpgfile):
    url = "https://www.googleapis.com/upload/drive/v3/files?uploadType=media"
    size = os.path.getsize(jpgfile)
    headers = {
        'Host':'www.googleapis.com',
        'Content-Type':'image/jpeg',
        'Content-Length': str(size),
        'Authorization': 'Bearer ' + credentials.access_token,
    }
    f = open(jpgfile, "rb")
    requests.post(url, headers=headers,data=f)

    return

def main():
    # 認証情報の取得
    credentials = get_credentials()

    # jpgfileのUpload(REST)
    upload_jpg(credentials, "sample.jpg")

if __name__ == '__main__':
    main()
'''

## 動作確認
'''
python google_drive_uploadjpg.py
'''

を実行して、GoogleDriveにイメージがアップロードされていればおkです

## おまけ：curlでUpload
認証情報を取得した後、~/.credentials/drive-python-quickstart.jsonに記載のaccess_tokenを直接入力すれば
curlでもUploadできます
'''uploadjpg_curl.sh
curl -X POST \
-H 'Host: www.googleapis.com' \
-H 'Content-Type: image/jpeg' \
-H 'Content-Length: number_of_bytes_in_file' \
-H 'Authorization: Bearer your_auth_token' \
-T sample.jpg \
https://www.googleapis.com/upload/drive/v3/files?uploadType=media
'''

number_of_bytes_in_fileにはsample.jpgのサイズを、
your_auth_tokenにはaccess_tokenを入力します

## ソースコード一式
以下に置きました。
ご自分のclient_secret.jsonを同じディレクトリに配置すると動作するはずです。
