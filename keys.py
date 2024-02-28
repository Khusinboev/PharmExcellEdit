import os
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


ADMIN_ID = [str(os.environ['ADMIN_ID1']), str(os.environ['ADMIN_ID2']), str(os.environ['ADMIN_ID3'])]
TOKEN = os.environ['BOT_TOKEN']


storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)


id_package_name = 'ИД упаковки'
trademark_name = 'Торговая марка'
inn_name = 'МНН'
manufacturer_name = 'Производитель'
medicine_packaging_name = 'Упаковка ЛП'
registration_number_name = 'Номер регистрации'
currency_name = 'Валюта'
limit_price_name = 'Предельная цена'
wholesale_price_name = 'Оптовая цена'
retail_price_name = 'Розничная цена'
date_name = 'Date'
