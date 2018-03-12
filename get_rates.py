import datetime
from datetime import date
from datetime import timedelta
from xml.etree import ElementTree

import requests

moex_date_mask = "%Y-%m-%d"
cbr_date_mask = "%d/%m/%Y"

today = date.today()
last_monday = today - timedelta(weeks=1, days=today.isoweekday() - 1)
last_sunday = last_monday + timedelta(weeks=1, days=-1)

val_RUABITR_close = None
val_MCFTRR_close = None
val_USD_rate = None

get_RUABITR_url = f"http://iss.moex.com/iss/history/engines/stock/markets/index/boards/RTSI/securities/RUABITR.json?from={last_monday}&till={last_sunday}"
response = requests.get(get_RUABITR_url).json()

if len(response['history']) > 0:
    if len(response['history']['data']) > 0:
        date = datetime.datetime.strptime(response['history']['data'][-1][2], moex_date_mask)
        val_RUABITR_close = response['history']['data'][-1][5]
    else:
        print("No data for RUABITR found!")
        exit(1)
else:
    print("No data for RUABITR found!")
    exit(1)

get_MCFTRR_url = f"http://iss.moex.com/iss/history/engines/stock/markets/index/boards/RTSI/securities/MCFTRR.json?from={date.strftime(moex_date_mask)}&till={date.strftime(moex_date_mask)}"
response = requests.get(get_MCFTRR_url).json()

if len(response['history']) > 0:
    if len(response['history']['data']) > 0:
        date = datetime.datetime.strptime(response['history']['data'][-1][2], moex_date_mask)
        val_MCFTRR_close = response['history']['data'][-1][5]
    else:
        print("No data for MCFTRR found!")
        exit(1)
else:
    print("No data for MCFTRR found!")
    exit(1)

get_USD_url = f"http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1={date.strftime(cbr_date_mask)}&date_req2={date.strftime(cbr_date_mask)}&VAL_NM_RQ=R01235"

response = requests.get(get_USD_url)
USD_rate_collection = ElementTree.fromstring(response.content)

for record in USD_rate_collection.findall('Record'):
    val_USD_rate = record.find('Value').text

print(f"Данные на {date.strftime(cbr_date_mask)}")
print(f"Курс рубля к доллару: {val_USD_rate} Р")
print(f"Индекс MCFTRR: {val_MCFTRR_close}".replace(".", ","))
print(f"Индекс RUABITR: {val_RUABITR_close}".replace(".", ","))
