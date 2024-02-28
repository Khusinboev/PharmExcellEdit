import pandas as pd
import psycopg2

from keys import id_package_name, trademark_name, manufacturer_name, inn_name, medicine_packaging_name, \
    registration_number_name, limit_price_name, currency_name, wholesale_price_name, retail_price_name, date_name


async def find_index(id_result_name, tolist_result):
    my_list_lower = [str(x).lower() for x in tolist_result]
    if id_result_name in tolist_result and tolist_result.index(id_result_name) is not None:
        id_result_id = tolist_result.index(id_result_name)
    else:
        lower_result = id_result_name.lower()
        try:
            id_result_id = my_list_lower.index(lower_result)
        except:
            if lower_result == 'date':
                id_result_id = my_list_lower.index(my_list_lower[-1])
            else:
                id_result_id = my_list_lower.index(lower_result+' (сум)')
    return id_result_id


async def InsertBase(msg, file_name):
    conn = psycopg2.connect(
        database="oson_ref_prod", user='postgres', password='@dmin2022', host='192.168.225.211', port='5432')
    conn.autocommit = True
    cur = conn.cursor()
    insert_query = f"""INSERT INTO "IO".ref_price ("ИД упаковки", "Торговая марка", "мнн", "производитель", "Упаковка ЛП", 
                        "Номер регистрации", "валюта", "Предельная цена", "Оптовая цена", "Розничная цена", "Date")
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    excel_file = f"fileDown/{file_name}"
    df = pd.read_excel(excel_file)
    insert_row = 0
    for index, row in df.iterrows():
        tolist = row.values.tolist()
        try:
            id_package_id = await find_index(id_result_name=id_package_name, tolist_result=tolist)
            trademark_id = await find_index(id_result_name=trademark_name, tolist_result=tolist)
            inn_id = await find_index(id_result_name=inn_name, tolist_result=tolist)
            manufacturer_id = await find_index(id_result_name=manufacturer_name, tolist_result=tolist)
            medicine_packaging_id = await find_index(id_result_name=medicine_packaging_name, tolist_result=tolist)
            registration_number_id = await find_index(id_result_name=registration_number_name, tolist_result=tolist)
            currency_id = await find_index(id_result_name=currency_name, tolist_result=tolist)
            limit_price_id = await find_index(id_result_name=limit_price_name, tolist_result=tolist)
            wholesale_price_id = await find_index(id_result_name=wholesale_price_name, tolist_result=tolist)
            retail_price_id = await find_index(id_result_name=retail_price_name, tolist_result=tolist)
            date_id = await find_index(id_result_name=date_name, tolist_result=tolist)
            break
        except:
            pass
    for index, row in df.iterrows():
        column1 = row[id_package_id]
        column2 = row[trademark_id]
        column3 = row[inn_id]
        column4 = row[manufacturer_id]
        column5 = row[medicine_packaging_id]
        column6 = row[registration_number_id]
        column7 = row[currency_id]
        column8 = row[limit_price_id]
        column9 = row[wholesale_price_id]
        column10 = row[retail_price_id]
        column11 = row[date_id]

        if insert_row != 0:
            values = (column1, column2, column3, column4, column5, column6, column7,
                      column8, column9, column10, column11)
            print(values)
            # cur.execute(insert_query, values)
            # conn.commit()
            insert_row += 1
            try:
                if insert_row % 100 == 0:
                    await msg.edit_text(f"Bazaga {insert_row} kiritildi")
            except:
                pass
        else:
            insert_row += 1

    try:
        await msg.edit_text(f"oxirgi amal bajarilmoqda...")
    except:
        pass

#     cur1 = cur.execute("""insert into "CRM"."ClientAppReference"(
#   "Guid",
#   "CreatedOn",
#   "CreatedBy",
#   "IsActive",
#   "ClientAppGuid",
#   "LinkedProductGuid",
#   "ProductName",
#   "ManufacturerName",
#   "Price",
#   "Rest",
#   "IsIgnored",
#   "Status",
#   "IsParapharm",
#   "IsOnlyForThisClient",
#   "IsChecked",
#   "ModifiedBySourceOn",
#   "LinkedSimilarity",
#   "NormalizedName",
#   "IsInGlobal")
# select
#  uuid_generate_v4() "Guid",
# now()  "CreatedOn",
# 'maziz'  "CreatedBy",
# true  "IsActive",
# '7fb0fd79-6f21-495f-84fd-b8bd1c31f362'  "ClientAppGuid",
#   null "LinkedProductGuid",
#   s."Упаковка ЛП" "ProductName",
#   s.производитель  "ManufacturerName",
#   s."Розничная цена" "Price",
#   1 "Rest",
#   false "IsIgnored",
#   0 "Status",
#   false "IsParapharm",
#   false "IsOnlyForThisClient",
#   false "IsChecked",
#   now() "ModifiedBySourceOn",
#   null "LinkedSimilarity",
# null  "NormalizedName",
#   false "IsInGlobal"
# from
#   "IO".ref_price s
# on conflict ("ClientAppGuid", "ProductName", "ManufacturerName") do nothing
# ;
#    """)
#     print(cur1)
#     cur2 = cur.execute(""" update "CRM"."ClientApp" set "LastSyncedDateTime" = now() where "Guid" = '7fb0fd79-6f21-495f-84fd-b8bd1c31f362' """)
#     print(cur2)
#     try:
#         await msg.edit_text(f"oxirgi amal bajarildi...")
#     except:
#         pass
#     cur.close()
#     conn.close()
    return insert_row


async def InsertBase2(excel_file):
    conn = psycopg2.connect(
        database="oson_ref_prod", user='postgres', password='@dmin2022', host='192.168.225.211', port='5432')
    conn.autocommit = True
    cur = conn.cursor()
    df = pd.read_excel(excel_file)

    insert_row = 0
    for index, row in df.iterrows():
        column1 = row["№"]
        column2 = row['Год']
        column3 = row["Наименование продукции"]
        column4 = row['Международное название продукта']
        column5 = row['Серия']
        column6 = row['Сертифицирующий орган']
        column7 = row['Фирма-производитель']
        column8 = row['Страна-производитель']
        column9 = row['По заказу']
        column10 = row['Регистрационный номер']
        column11 = row['Номер бланка']
        column12 = row['Дата выдачи сертификата']

        insert_query = f"""INSERT INTO "IO".sertifikat("№", год, "Наименование продукции", "Международное название продукта", 
                     серия, "Сертифицирующий орган", "Фирма-производитель", "Страна-производитель", "По заказу", 
                     "Регистрационный номер", "Номер бланка", "Дата выдачи сертификата") 
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (column1, column2, column3, column4, column5, column6, column7,
                  column8, column9, column10, column11, column12)

        cur.execute(insert_query, values)
        conn.commit()
        insert_row += 1

    cur.execute("""
insert into "CRM"."ClientAppReference"(
  "Guid",
  "CreatedOn",
  "CreatedBy",
  "IsActive",
  "ClientAppGuid",
  "LinkedProductGuid",
  "ProductName",
  "ManufacturerName",
  "Price",
  "Rest",
  "IsIgnored",
  "Status",
  "IsParapharm",
  "IsOnlyForThisClient",
  "IsChecked",
  "ModifiedBySourceOn",
  "LinkedSimilarity",
  "NormalizedName",
  "IsInGlobal")
select
 uuid_generate_v4() "Guid",
now()  "CreatedOn",
'bot'  "CreatedBy",
true  "IsActive",
'35da65bf-e276-4cb3-ad9e-38d6a0aae05a'  "ClientAppGuid",
  null "LinkedProductGuid",
  s."Наименование продукции" "ProductName",
  s."Фирма-производитель" "ManufacturerName",
  1 "Price",
  1 "Rest",
  false "IsIgnored",
  0 "Status",
  false "IsParapharm",
  false "IsOnlyForThisClient",
  false "IsChecked",
  now() "ModifiedBySourceOn",
  null "LinkedSimilarity",
null  "NormalizedName",
  true "IsInGlobal"
from
  "IO".sertifikat s
group by
  s."Наименование продукции",
  s."Фирма-производитель"
on conflict ("ClientAppGuid", "ProductName", "ManufacturerName") do nothing  
;   """)

    cur.execute("""update "CRM"."ClientApp" 
set "LastSyncedDateTime" = now()
where "Guid" = '35da65bf-e276-4cb3-ad9e-38d6a0aae05a'""")

    cur.close()
    conn.close()

    return insert_row
