# Google-sheets data
import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials
import gspread

import time
import asyncio

CREDENTIALS_FILE = 'cred.json'
spreadsheet_id = '139VvQrniwAtk93hsBsYUQnA_iOcXevzXTrlNkpEsFcI' 
# 139VvQrniwAtk93hsBsYUQnA_iOcXevzXTrlNkpEsFcI - prod
# 1Tp-tozyuFBIeuN6-nvYZXchVpXu9MsNbjiQyLB7JQzg - my sheets

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ])

httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)

async def writeOne(list_, row_id, col_id, data):
    # Преобразуем числовые индексы строк и столбцов в буквенные обозначения
    range_ = gspread.utils.rowcol_to_a1(row_id, col_id)
    # Вписываем значение
    res = service.spreadsheets().values().batchUpdate(
        spreadsheetId = spreadsheet_id,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {
                    "range": f"{list_}!{range_}",
                    "majorDimension": "ROWS",
                    "values": [[f"{data}"]]
                }
            ]
        }
    ).execute()
    return res
    

async def readRange(list_, range_):
    for i in range(10):
        try:
            values = service.spreadsheets().values().get(
                spreadsheetId = spreadsheet_id,
                range = f"{list_}!{range_}",
                majorDimension = 'COLUMNS'
            ).execute()
            values = values["values"]
            return values
        except Exception as e:
            if "HttpError 429" in str(e):
                print("GOT ERROR")
                await asyncio.sleep(2)
                continue
            else:
                values = []
                break
    return values


async def readOne(list_, row_id, col_id):
    for i in range(20):
        try:
            range_ = gspread.utils.rowcol_to_a1(row_id, col_id)
            values = service.spreadsheets().values().get(
                spreadsheetId = spreadsheet_id,
                range = f"{list_}!{range_}",
                majorDimension = 'COLUMNS'
            ).execute()
            values = values["values"]
            return values
        except Exception as e:
            if "HttpError 429" in str(e):
                print("GOT ERROR")
                await asyncio.sleep(2)
                continue
            else:
                values = []
                break
    return values


async def colorCell(list, row_id, col_id):
    
    cell_range = gspread.utils.rowcol_to_a1(row_id, col_id)

    # Цвет, которым вы хотите закрасить ячейку (RGB)
    cell_format = {
        "userEnteredFormat": {
            "backgroundColor": {
                "red": 1.0,   # Укажите красный цвет (от 0 до 1)
                "green": 0.0, # Укажите зеленый цвет (от 0 до 1)
                "blue": 0.0   # Укажите синий цвет (от 0 до 1)
            }
        }
    }

    # Задание формата ячейки
    body = {
        "repeatCell": {
            "range": {
                "sheetId": 0,  # Замените на ID листа, если необходимо
                "startRowIndex": 0,  # Начальная строка (0 для A1)
                "endRowIndex": 1,    # Конечная строка (1 для цветовой заливки A1)
                "startColumnIndex": 0,  # Начальный индекс колонки (0 для A)
                "endColumnIndex": 1   # Конечный индекс колонки (1 для закраски A)
            },
            "cell": cell_format,
            "fields": "userEnteredFormat(backgroundColor)"
        }
    }

    # Отправляем запрос на обновление ячейки с нужным цветом
    response = service.spreadsheets().batchUpdate(
            spreadsheetId = spreadsheet_id, 
            body=body
        ).execute()
    return 0