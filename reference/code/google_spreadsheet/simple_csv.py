import csv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from time import sleep

LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
           'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
TMP_CSV_FILE = "csv_sample/csv_sample_copy.csv"

# Gspread Setting
SPREADSHEET_KEY = '18jf-W56QqMvjSUgvxBv76Hm3H-HEmgkUZTz-7_Qx1F8'  # 共有設定したスプレッドシートキー
SCOPE = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
KEY_PATH = '/home/pi/Key/creeks-1574788873145-ecb1ac12ac88.json'


def read_tmp_csv():
    with open(TMP_CSV_FILE, 'r') as f:
        reader = csv.reader(f)
        csv_data = [row for row in reader]
    return csv_data


def recreate_tmp_csv():
    with open(TMP_CSV_FILE, 'r') as f:
        print('Recreated TMP CSV ')


def write_spreadsheet():
    # gspread Setting
    print("Start gspread setting...")
    try:
        CREDENTIALS = ServiceAccountCredentials.from_json_keyfile_name(
            KEY_PATH, SCOPE)
        GC = gspread.authorize(CREDENTIALS)
        # 共有設定したスプレッドシートのシート１を開く
        WORKSHEET = GC.open_by_key(SPREADSHEET_KEY).sheet1
        print("Finish gspread setting")
    except:
        print("Error: gspread setting")
        return None

    try:
        index = 1
        while True:
            num = str(index)
            Acell = 'A' + num
            if not WORKSHEET.acell(Acell).value:
                break
            index += 1

        csv_data = read_tmp_csv()
        for data in csv_data:
            data_num = len(data)
            for i in range(data_num):
                row_id = LETTERS[i]  # A,B,C,D,E,F,G...
                cell = row_id + num  # A15, B15, C15, ...
                WORKSHEET.update_acell(cell, data[i])
            num = str(int(num) + 1)
            sleep(10)
        recreate_tmp_csv()
        print("Finish writing spreadsheet")
    except:
        print("Error: writing spreadsheet")
