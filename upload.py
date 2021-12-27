import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(credentials)

spreadsheet = client.open('Red flags KYRGYZSTAN(copy)')
table_names = ['parties.csv']

for name in table_names:
    spreadsheet.add_worksheet(f'{name}', cols=25, rows=100, index=0)
    with open(f'flattened/{name}', 'r', encoding="utf8") as file_obj:
        content = file_obj.read()
    body = {
        "requests": [
            {
                "pasteData": {
                    "coordinate": {
                        "sheetId": spreadsheet.worksheet(f'{name}').id,
                        "rowIndex": 0,
                        "columnIndex": 0,
                    },
                    "data": content,
                    "type": "PASTE_NORMAL",
                    "delimiter": ",",
                }
            }
        ]
    }

    spreadsheet.batch_update(body)
#    client.import_csv(spreadsheet.id, data=content)




