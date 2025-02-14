import gspread
from oauth2client.service_account import ServiceAccountCredentials
import fun

CREDENTIALS_FILE = 'gs_credentials.json'


def load_bas_price():
    # Подсоединение к Google Таблицам
    scope = ['https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive"]

    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
    client = gspread.authorize(credentials)

    spreadsheet = client.open(fun.FILE_NAME)
    worksheet = spreadsheet.worksheet('Bas')

    range_url = fun.RANGE_URL
    range_c = fun.RANGE_C

    url_values = worksheet.get(range_url)  # Читаем данные из диапазона
    name = 'div'
    att = {'class': 'price'}
    site_price = fun.get_site_price(url_values, name, att)

    result = []
    for price in site_price:
        result.append([price])
    print(result)
    worksheet.update(range_c, result)