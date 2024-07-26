import gspread
from google.oauth2.service_account import Credentials

SHEET = None

def init_storage():
    global SHEET

    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_file('creds.json')
    scope_creds = creds.with_scopes(scope)
    client = gspread.authorize(scope_creds)
    SHEET = client.open('twizy')

def get_column(worksheet_name, col_num):
    page = SHEET.worksheet(worksheet_name)
    return [i for i in page.col_values(col_num)[1:]]

def set_column(worksheet_name, col_num, data):
    page = SHEET.worksheet(worksheet_name)
    r = column_to_range(col_num, data)
    page.update(r, data)

def column_to_range(col_num, data):
    letter_code = ord('A') + col_num - 1
    letter = chr(letter_code)
    return f"{letter}2:{letter}{len(data) + 1}"

def get_table(worksheet_name):
    page = SHEET.worksheet(worksheet_name)
    return [[row for row in col] for col in page.get_all_values()]

def set_table(worksheet_name, table):
    start_letter = 'A'
    end_letter = chr(ord('A') + len(table[0]) - 1)
    r = f"{start_letter}2:{end_letter}{len(table) + 1}"
    page = SHEET.worksheet(worksheet_name)
    page.update(r, table)