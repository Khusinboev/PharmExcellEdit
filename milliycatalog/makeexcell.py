import json
import time
from urllib.parse import urlparse
from keys import bot, dp

import keys
import requests
import xlsxwriter
from bs4 import BeautifulSoup
from collections import Counter
from mylist import s


def get_url2(url):
    response = requests.get(url).text
    soup = BeautifulSoup(response, "lxml").find_all('div', class_="catalog__grid-view__item products-slider__item col-sm-6 wrap wrap-sm-2 col-lg-4 wrap-lg-3")
    return soup


def get_url3(url):
    response = requests.get(url).text
    soup = BeautifulSoup(response, "lxml").find_all('ul', class_="pagination category-pagination")
    return soup


def get_url4(url):
    response = requests.get(url).text
    soup = BeautifulSoup(response, "lxml").find_all('div', class_='tab-section')
    return soup


def is_link(text):
    time.sleep(1)
    parsed = urlparse(text)
    return bool(parsed.scheme and parsed.netloc)


def makeexcell(fileName, chat_id):
    col_counter = 0
    col_dict = dict()
    row = 0
    workbook = xlsxwriter.Workbook(f'{fileName}.xlsx')
    worksheet = workbook.add_worksheet()
    counts = Counter(s)
    mylist = list(counts.keys())
    for link in mylist:
        print(link)
        link = link
        row += 1
        for i in get_url4(link)[1:][:-1]:
            heading = i.find('div', class_='tab-section__heading')
            if heading is None:
                pass
            else:
                heading = heading.text.strip()
                names = i.find_all('th')
                values = i.find_all('td')
                old_name = ''
                name_counter = 0
                for name, value in zip(names, values):
                    name = name.text.strip()
                    value = value.text.strip()
                    if is_link(value):
                        value = '#' + value
                    if name == '' or not name:
                        name_counter += 1
                        name = old_name + ' #' + str(name_counter)
                    else:
                        old_name = name
                        name_counter = 0
                    if (heading + ' - ' + name) in col_dict:
                        col_number = col_dict[heading + ' - ' + name]
                    else:
                        col_dict[heading + ' - ' + name] = col_counter
                        col_number = col_counter
                        worksheet.write(0, col_counter + 1, heading + ' - ' + name)
                        col_counter = col_counter + 1
                    worksheet.write(0, 0, "Urls")
                    worksheet.write(row, 0, '#' + link)
                    worksheet.write(row, col_number + 1, value)
        if row % 3000 == 0:
            time.sleep(10)
    workbook.close()

    document = open("data.xlsx", "rb")
    url = f"https://api.telegram.org/bot{keys.API_TOKEN}/sendDocument"
    response = requests.post(url, data={'chat_id': chat_id}, files={'document': document})
    content = response.content.decode("utf8")
    js = json.loads(content)
    print(js)


makeexcell(fileName='data', chat_id=1918760732)
