import gspread
from oauth2client.service_account import ServiceAccountCredentials
import fun

CREDENTIALS_FILE = 'gs_credentials.json'

def load_bas_price(sheet_name, name, att):
  # Подсоединение к Google Таблицам
  scope = ['https://www.googleapis.com/auth/spreadsheets',
           "https://www.googleapis.com/auth/drive"]

  credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
  client = gspread.authorize(credentials)

  spreadsheet = client.open(fun.FILE_NAME)
  worksheet = spreadsheet.worksheet(sheet_name)

  url_values = worksheet.get(fun.RANGE_URL) # Читаем данные из диапазона
  site_price = fun.get_site_price(url_values, name, att)
  fun.write_result(site_price, worksheet)