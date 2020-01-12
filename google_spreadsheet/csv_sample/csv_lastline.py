import csv
import gspread
import json

from oauth2client.service_account import ServiceAccountCredentials 

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('/home/pi/Key/creeks-1574788873145-ecb1ac12ac88.json', scope)

gc = gspread.authorize(credentials)

SPREADSHEET_KEY = '18jf-W56QqMvjSUgvxBv76Hm3H-HEmgkUZTz-7_Qx1F8'

#共有設定したスプレッドシートのシート1を開く
worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1

index = 1
while True:
    if not worksheet.acell('A'+str(index)).value:
        with open('csv_sample.csv') as f:
            reader = f.readlines()
            last_row = len(reader) - 1
            row = reader[last_row].replace('\n','').split(',')

            num = str(index)
            
            c_list = ['A', 'B', 'C', 'D','E']
            for i,c in enumerate(c_list):
                cell = c + num
                worksheet.update_acell(cell, row[i])
            print('num: ' + num)
            print(row)
        break
    index += 1
