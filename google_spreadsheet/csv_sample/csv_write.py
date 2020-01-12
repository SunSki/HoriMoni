import csv
import gspread
import json

#ServiceAccountCredentials：Googleの各サービスへアクセスできるservice変数を生成します。
from oauth2client.service_account import ServiceAccountCredentials 

#2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

#認証情報設定
#ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
credentials = ServiceAccountCredentials.from_json_keyfile_name('/home/pi/Key/creeks-1574788873145-ecb1ac12ac88.json', scope)

#OAuth2の資格情報を使用してGoogle APIにログインします。
gc = gspread.authorize(credentials)

#共有設定したスプレッドシートキーを変数[SPREADSHEET_KEY]に格納する。
SPREADSHEET_KEY = '18jf-W56QqMvjSUgvxBv76Hm3H-HEmgkUZTz-7_Qx1F8'

#共有設定したスプレッドシートのシート1を開く
worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1

data = [1,2,3]

index = 1
while True:
    if not worksheet.acell('A'+str(index)).value:
        with open('csv_sample.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                num = str(index)
                Acell = 'A' + num
                Bcell = 'B' + num
                Ccell = 'C' + num
                worksheet.update_acell(Acell, row[0])
                worksheet.update_acell(Bcell, row[1])
                worksheet.update_acell(Ccell, row[2])
                print('num: ' + num)
                print(row)
                index += 1
        break
    index += 1
