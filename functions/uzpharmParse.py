import json
import pytz
import aiohttp
import datetime
import xlsxwriter


async def get_site_content1(URL):
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as resp:
            text = await resp.read()
            text = json.loads(text)
    return text


async def uz_pharm_parse():
    workbook = xlsxwriter.Workbook('uzpharmDown/uzpharm.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write('A1', '№')
    worksheet.write('B1', 'Год')
    worksheet.write('C1', 'Наименование продукции')
    worksheet.write('D1', 'Международное название продукта')
    worksheet.write('E1', 'Серия')
    worksheet.write('F1', 'Сертифицирующий орган')
    worksheet.write('G1', 'Фирма-производитель')
    worksheet.write('H1', 'Страна-производитель')
    worksheet.write('I1', 'По заказу')
    worksheet.write('J1', 'Регистрационный номер')
    worksheet.write('K1', 'Номер бланка')
    worksheet.write('L1', 'Дата выдачи сертификата')

    k = 1

    info2 = await get_site_content1(
        f"""https://uzpharm-control.uz/registries/certified_medicines/server-response.php?
        columns%5B11%5D%5Bdata%5D=sert_date&columns%5B11%5D%5Borderable%5D=true&order%5B0%5D%5Bcolumn%5D=11&
        order%5B0%5D%5Bdir%5D=desc&start=0&length=11000""")

    infoAll = info2["data"]
    print(len(infoAll))

    for i in infoAll:
        if int(i["sert_date"][3:5]) != 1:
            if int(i["sert_date"][3:5]) >= (int(datetime.datetime.now(pytz.timezone('Asia/Tashkent')).strftime('%m'))-2):
                k += 1
                worksheet.write(f'A{k}', i['DT_RowId'])
                worksheet.write(f'B{k}', i['year'])
                worksheet.write(f'C{k}', i['title'])
                worksheet.write(f'D{k}', i['title_2'])
                worksheet.write(f'E{k}', i['series'])
                worksheet.write(f'F{k}', i['sert_org'])
                worksheet.write(f'G{k}', i['manufacturer'])
                worksheet.write(f'H{k}', i['country'])
                worksheet.write(f'I{k}', i['customer'])
                worksheet.write(f'J{k}', i['reg_num'])
                worksheet.write(f'K{k}', i['blank_num'])
                worksheet.write(f'L{k}', i['sert_date'])
        else:
            if int(i["sert_date"][3:5]) >= 12:
                k += 1
                worksheet.write(f'A{k}', i['DT_RowId'])
                worksheet.write(f'B{k}', i['year'])
                worksheet.write(f'C{k}', i['title'])
                worksheet.write(f'D{k}', i['title_2'])
                worksheet.write(f'E{k}', i['series'])
                worksheet.write(f'F{k}', i['sert_org'])
                worksheet.write(f'G{k}', i['manufacturer'])
                worksheet.write(f'H{k}', i['country'])
                worksheet.write(f'I{k}', i['customer'])
                worksheet.write(f'J{k}', i['reg_num'])
                worksheet.write(f'K{k}', i['blank_num'])
                worksheet.write(f'L{k}', i['sert_date'])

    workbook.close()
    return "tamom"
