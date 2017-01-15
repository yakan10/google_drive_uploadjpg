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

    :return: 取得された認証情報

    ・そのまま実行すると自動でブラウザが開いて認証画面に飛ぶ
    ・--noauth_local_webserver オプションをつけるとコンソールにURLが表示される
      表示されたURLをブラウザに入力すると認証画面が表示され、認証後出てきたコードをコンソール上で入力する
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
