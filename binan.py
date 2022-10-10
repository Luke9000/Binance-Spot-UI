import math
from tkinter import messagebox, END
from binance.client import Client
from binance.enums import *
import decimal
import config
from datetime import datetime



def cur_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S ")
    return current_time

try:
    client = Client(config.apiKey, config.apiSecurity)
    print("connected")
except Exception as ex:
    print("connection_error: ", ex)

def getData(symbol, bnb_label, deals_label, bank):
    info = client.get_symbol_info(symbol)
    tick = decimal.Decimal(info['filters'][0]['tickSize'].rstrip("0"))
    step = decimal.Decimal(info['filters'][2]['stepSize'].rstrip("0"))
    # ---------------------------------------------------------
    qtyExponent = - step.as_tuple().exponent
    tickExponent = - tick.as_tuple().exponent
    # ---------------------------------------------------------
    config.tickSize = tick
    config.stepSize = step
    config.qtyExponent = qtyExponent
    config.tickExponent = tickExponent
    # ---------------------------------------------------------
    bnb_price = float(client.get_avg_price(symbol='BNBUSDT')['price'])
    bnb = float(client.get_asset_balance(asset='BNB')['free'])
    bnb_balance = round(bnb * bnb_price, 2)
    bnb_label.configure(text =  bnb_balance)
    deals_left = int(bnb * bnb_price / (float(bank) * 0.0015))
    deals_label.configure(text = deals_left)
    # ---------------------------------------------------------
    print("tickSize: ", config.tickSize)
    print("stepSize: ", config.stepSize)
    print("qtyExponent: ", config.qtyExponent)
    print("tickExponent: ", config.tickExponent)
    print("tick- price, step - quantity")

    # ---------------------------------------------------------


def buy(symbol, price, quantity, entry):
    try:
        buy_order = client.create_order(
            symbol=symbol,
            side=SIDE_BUY,
            type=ORDER_TYPE_LIMIT,
            price=price,
            quantity=quantity,
            timeInForce='FOK'
        )
        print(cur_time(), "buy_order: ", buy_order)
        if buy_order['status'] == "FILLED":
            entry.delete(0, END)
    except Exception as e:
        print("buy_error: ",e ,"price: ", price, "quantity: ", quantity)
#---------------------------------------------------------
#Example
#BuyButton = Button(root,text = "Buy", command = lambda: buy(Symbol.get(),Price.get(),Quantity.get()))
#---------------------------------------------------------


def sell(symbol, stop, limit, quantity):
    if stop > limit:
        try:
            sell_order = client.create_order(
                symbol=symbol,
                side=SIDE_SELL,
                type=ORDER_TYPE_STOP_LOSS_LIMIT,
                stopPrice=stop,
                quantity=quantity,
                timeInForce='GTC',
                price=limit
            )
            print(cur_time(), "sell_order: ", sell_order)
            config.orderId = sell_order['orderId']
        except Exception as e2:
            print("sell_error: ",e2,"stop: ", stop, "limit: ", limit, "quantity:", quantity )
    else:
        messagebox.showinfo("Bad input", "Limit must be less than Stop")

#---------------------------------------------------------
#example
#sell('BTCUSDT',20000,0.0006,19000)
#---------------------------------------------------------


def sell_oco(symbol, price, stop, limit, quantity):
    if stop > limit:
        try:
            sell_order = client.order_oco_sell(
                symbol=symbol,
                price=price,
                stopPrice=stop,
                stopLimitPrice=limit,
                quantity=quantity,
                stopLimitTimeInForce='GTC'
            )
            print(cur_time(), "oco_sell_order: ", sell_order)
            config.orderId = sell_order['orders'][0]['orderId']
            config.orderId2 = sell_order['orders'][1]['orderId']
            print(sell_order)
        except Exception as e:
            print(cur_time(), "oco_sell_error: ", e, "price: ", price, "stop: ", stop, "limit: ", limit, "quantity:", quantity )
    else:
        messagebox.showinfo("Bad input", "Limit must be less than Stop")

#---------------------------------------------------------
#example
#sell('BTCUSDT',20000,0.0006,19000)
#---------------------------------------------------------



def cancel(symbol):
    try:
        cancelorder = client.cancel_order(
            symbol=symbol,
            orderId=config.orderId
        )
        print(cur_time(), "cancel_order: ", cancelorder)
    except Exception as e1:
        print("cancel_error: ", e1)
#---------------------------------------------------------
#example
#
#---------------------------------------------------------



def cancel_oco(symbol):
    try:
        cancelorder = client.cancel_order(
            symbol=symbol,
            orderId=config.orderId
        )
        print(cur_time(), "cancel_order_oco_1: ", cancelorder)
    except Exception as e1:
        print("cancel_error_oco_1: ", e1)
    try:
        cancelorder2 = client.cancel_order(
            symbol=symbol,
            orderId=config.orderId2
        )
        print(cur_time(), "cancel_order_oco_2: ", cancelorder2)
    except Exception as e2:
        print("cancel_error_oco_2: ", e2)
#---------------------------------------------------------
#example
#
#---------------------------------------------------------


def buystoploss(symbol, price, stop, limit, quantity, entry):
    if stop > limit:
       buy(symbol, price, quantity, entry)
       sell(symbol, stop, limit, quantity)
       entry.delete(0, END)
    else:
        messagebox.showinfo("Bad input", "Limit must be less than Stop")
#---------------------------------------------------------
#example
#
#---------------------------------------------------------



def ocobuystoploss(symbol, price, sell_price, stop, limit, quantity, entry):
    if stop > limit:
       buy(symbol, price, quantity, entry)
       sell_oco(symbol,sell_price, stop, limit, quantity)
       entry.delete(0, END)
    else:
        messagebox.showinfo("Bad input", "Limit must be less than Stop")
#---------------------------------------------------------
#example
#
#---------------------------------------------------------


def upgrade(symbol, stop, limit, quantity):
    print("cancel OrderId: ", config.orderId)
    cancel(symbol)
    sell(symbol, stop, limit, quantity)
#---------------------------------------------------------
#example
#
#---------------------------------------------------------


def upgrade_oco(symbol, price, stop, limit, quantity):
    cancel_oco(symbol)
    sell_oco(symbol, price, stop, limit, quantity)
#---------------------------------------------------------
#example
#
#---------------------------------------------------------


def autolimit(stop, entry):
    try:
        entry.delete(0, END)
        entry.insert(0, round(decimal.Decimal(stop) * decimal.Decimal(0.9),  config.tickExponent))
    except Exception as e:
        print("autolimit error: ", e)
#---------------------------------------------------------
#example
#
#---------------------------------------------------------


def autoquantity(bank, price, entry):
    try:
        entry.delete(0, END)
        entry.insert(0, round(decimal.Decimal(bank) / decimal.Decimal(price), config.qtyExponent))
    except Exception as e:
        print("autoquantity error: ", e)
#---------------------------------------------------------
#example
#
#---------------------------------------------------------


def autostop(stop, entry):
    tick = config.tickSize
    try:
        entry.delete(0, END)
        entry.insert(0, decimal.Decimal(stop) + tick)
    except Exception as e:
        print("autostop error: ", e)
#---------------------------------------------------------
#example
#
#---------------------------------------------------------



def autostop3x(stop, entry):
    tick = config.tickSize
    try:
        entry.delete(0, END)
        entry.insert(0, decimal.Decimal(stop) + 3 * tick)
    except Exception as e:
        print("autostop3x error: ", e)
#---------------------------------------------------------
#example
#
#---------------------------------------------------------




