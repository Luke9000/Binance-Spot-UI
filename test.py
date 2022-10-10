import decimal

from binance.client import Client
from binance.enums import *
import config
from datetime import datetime
client = Client(config.apiKey, config.apiSecurity)
print("connected")

info2 = client.get_account()
#print(info2)
#print(info2['balances'])
#print(info['filters'][0]['tickSize'])



bnb_price = client.get_avg_price(symbol='BNBUSDT')['price']
#print(avg_price['price'])
#print(avg_price)