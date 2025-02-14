import datetime
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials

CREDENTIALS_FILE = 'gs_credentials.json'
FILE_NAME = "price_control"
RANGE_URL = 'B2:B109'
RANGE_C = 'C2:C109'
TIME_CELL = 'G1'

def get_site_price(url_values, name, att):
    site_price = []
    for url in url_values:
        if len(url) == 1:
            page_link = url[0]
            response = requests.get(page_link, headers={'User-Agent': UserAgent().chrome})
            # считываем текст HTML-документа
            src = response.content
            # print(response)

            soup = BeautifulSoup(src, 'html.parser')

            # obj = soup.find('div', attrs = {'class':'price'})
            obj = soup.find(name=name, attrs=att)
            if obj is None:
                site_price.append(0)
            else:
                print(obj.text)
                site_price.append(obj.text)
        else:
            site_price.append("-")
    return site_price

def write_result(site_price, worksheet):
    day = datetime.datetime.now().strftime('%d %B %Y %X')
    worksheet.update_acell(TIME_CELL, value=day)
    result = []
    for price in site_price:
        result.append([price])
    print(result)
    worksheet.update(RANGE_C, result)

def load_price(sheet_name, name, att):
  # Подсоединение к Google Таблицам
  scope = ['https://www.googleapis.com/auth/spreadsheets',
           "https://www.googleapis.com/auth/drive"]

  credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
  client = gspread.authorize(credentials)

  spreadsheet = client.open(FILE_NAME)
  worksheet = spreadsheet.worksheet(sheet_name)

  url_values = worksheet.get(RANGE_URL) # Читаем данные из диапазона
  site_price = get_site_price(url_values, name, att)
  write_result(site_price, worksheet)