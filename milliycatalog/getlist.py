from bs4 import BeautifulSoup
import lxml
import requests
import time
# from milliycatalog.makeexcell import makeexcell


def get_category_url(url):
    try:
        response = requests.get(url).text
        soap = BeautifulSoup(response, "lxml")
        category_div = soap.find('div', class_="category-main__sidebar")
        if category_div:
            if category_div is None:
                url_list = []
            url_list = category_div.find_all('a')
        else:
            url_list = []
        return url_list
    except Exception as ex:
        print('m')
        time.sleep(30)
        get_category_url(url)


def get_product_url(url):
    try:
        response = requests.get(url).text
        soap = BeautifulSoup(response, "lxml")
        product_grid = soap.find('div', class_="catalog__grid-view")
        if product_grid:
            product_url_list = product_grid.find_all('a', class_="link-gray")
            if product_url_list is None:
                product_url_list = []
        else:
            product_url_list = []
        return product_url_list
    except Exception as ex:
        time.sleep(30)
        get_product_url(url)


# @multitasking.task
async def getlistall(user_id):
    main_url = "https://catalog.milliykatalogi.uz"
    product_list = []
    category_url_list = list({"/212-preparaty-farmacevticheskie-1/"})
    n = 0

    c_list = []
    while len(category_url_list) > 0:
        url = category_url_list.pop()
        new_urls = get_category_url(main_url+url)
        if n == 10:
            break
        if len(new_urls) == 0:
            c_list.append(main_url+url)
            page = 1
            while True:
                print(page)
                if page % 50 == 0:
                    time.sleep(10)
                product_urls = get_product_url(main_url+url+'/page'+str(page)+'/')
                if len(product_urls) == 0:
                    break
                page = page + 1
                for x in product_urls:
                    product_list.append(main_url+x['href'])
        else:
            category_url_list = category_url_list + (list(x['href'] for x in new_urls))
    print(len(product_list))
    with open('milliycatalog/mylist.py', 'w') as f:
        f.write('s = ' + str(product_list))
    time.sleep(100)
    print("list yasaldi")
    # makeexcell(fileName='data', chat_id=1918760732)
