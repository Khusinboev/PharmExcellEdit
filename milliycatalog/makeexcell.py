import time
from urllib.parse import urlparse
import json
from keys import bot, dp
import pandas as pd
import psycopg2
import keys
import requests
import xlsxwriter
from bs4 import BeautifulSoup
from collections import Counter

import asyncio


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
    parsed = urlparse(text)
    return bool(parsed.scheme and parsed.netloc)


async def makeexcell(fileName, chat_id, s):
    msg_id = 0
    token = keys.API_TOKEN
    chat_id = chat_id
    url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + f"?chat_id={chat_id}" + "&text=" + "asa boshladiq" 
    req = requests.get(url_req)
    if req.ok is True:
        msg_id = int(req.json()['result']['message_id'])
    try:
        col_counter = 0
        col_dict = dict()
        row = 0
        workbook = xlsxwriter.Workbook(f'{fileName}.xlsx')
        worksheet = workbook.add_worksheet()
        counts = Counter(s)
        mylist = list(counts.keys())
        for link in mylist:
            time.sleep(0.5)
            if msg_id != 0 and row % 5 == 0:
                url_req = "https://api.telegram.org/bot" + token + "/editMessageText" + f"?chat_id={chat_id}" + f"&message_id={msg_id}" + "&text=" + str(row) 
                requests.get(url_req)
            elif msg_id == 0:
                url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + f"?chat_id={chat_id}" + "&text=" + str(row)
                req = requests.get(url_req)
                if req.ok is True:
                    msg_id = int(req.json()['result']['message_id'])
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
        document = open("/home/pharmeditexcel-bot/data.xlsx", "rb")
        url = f"https://api.telegram.org/bot{keys.API_TOKEN}/sendDocument"
        response = requests.post(url, data={'chat_id': chat_id}, files={'document': document})
        content = response.content.decode("utf8")
        req = json.loads(content)


        conn = psycopg2.connect(
        database="oson_ref_prod", user='postgres', password='@dmin2022', host='192.168.225.211', port='5432')
        conn.autocommit = True
        cur = conn.cursor()
        excel_file = "/home/pharmeditexcel-bot/data.xlsx"
        df = pd.read_excel(excel_file)
        for row in df.iterrows():
            try:
                column1 = row[1]["Идентификация товара - Торговое наименование товара"]
                column2 = row[1]["Владелец идентификатора товара (GTIN) - Наименование компании"]
                column3 = row[1]["Потребительская упаковка - Код товара упаковки"]
                column4 = row[1]["Urls"]

                insert_query = f"""INSERT INTO "IO".milliy_katalog ("Идентификация товара - Торговое наименование товара", 
                                                                    "Владелец идентификатора товара (GTIN) - Наименование компании", 
                                                                    "Потребительская упаковка - Код товара упаковки",
                                                                    "Urls") 
                                VALUES (%s, %s, %s, %s)"""
                values = (column1, column2, column3, column4)
                cur.execute(insert_query, values)
                conn.commit()
            except Exception as ex:
                pass
        
        cur.execute("""INSERT INTO "CRM"."ClientAppReference"
        ("Guid", "CreatedOn", "CreatedBy", "IsActive", "ClientAppGuid", "ProductName", "ManufacturerName", "Price", "Rest", "IsIgnored", "Status", "IsParapharm", "IsOnlyForThisClient", "IsChecked")
        select
        uuid_generate_v4() "Guid",
        now() "CreatedOn",
        'maziz' "CreatedBy",
        true "IsActive",
        '098d00ce-81b0-4dac-a1c6-0dda5cc68101' "ClientAppGuid",
        c."Идентификация товара - Торговое на" "ProductName",
        c."Владелец идентификатора товара (GTI" "ManufacturerName",
        1 "Price",
        1 "Rest",
        false "IsIgnored",
        0 "Status",
        false "IsParapharm",
        false "IsOnlyForThisClient",
        false "IsChecked"
        from
        "IO".milliy_katalog  c
        on conflict ("ClientAppGuid", "ProductName", "ManufacturerName") do nothing;

        update "CRM"."ClientApp" 
        set "LastSyncedDateTime" = now()
        where "Guid" = '098d00ce-81b0-4dac-a1c6-0dda5cc68101' """)
        s = conn.commit()
        print(s)
        
        url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + f"?chat_id={chat_id}" + "&text=" + "malumotlar bazaga tiqildi, tekshirib ko'rishingiz mumkin" 
        req1 = requests.get(url_req)
        print(req1)

    except Exception as e:
        url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + f"?chat_id={chat_id}" + "&text=" + str(e)
        req = requests.get(url_req)

    loop = asyncio.get_running_loop()
    loop.stop()