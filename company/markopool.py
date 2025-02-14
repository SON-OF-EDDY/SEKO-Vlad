import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
import re
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

CREDENTIALS_FILE = 'gs_credentials.json'

def load_markopool_price():
  # Подсоединение к Google Таблицам
  scope = ['https://www.googleapis.com/auth/spreadsheets',
           "https://www.googleapis.com/auth/drive"]

  credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
  client = gspread.authorize(credentials)

  spreadsheet = client.open("price_control")
  worksheet = spreadsheet.worksheet('Markopool')

  range_url = 'B2:B109'
  range_c = 'C2:C109'
  # Читаем данные из диапазона
  url_values = worksheet.get(range_url)


  site_price = []
  for url in url_values:
    if len(url) == 1:
      page_link = url[0]
      response = requests.get(page_link, headers={'User-Agent': UserAgent().chrome})
      # считываем текст HTML-документа
      src = response.content
      # print(response)

      soup = BeautifulSoup(src, 'html.parser')

      obj = soup.find('span', attrs = {'class':'product-card-page__new-price-card'})
      print(obj.text)
      site_price.append(obj.text)
    else:
      site_price.append(0)

  # Записываем данные в ячейку/ Сюда записать дату обновления
  # worksheet.update_acell('C1', price)
  # Записываем данные в диапазон

  result = []
  for price in site_price:
    result.append([price])
  print(result)
  worksheet.update(range_c, result)