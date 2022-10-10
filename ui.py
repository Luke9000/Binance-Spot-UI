from tkinter import *
from binan import *


def uiInit():
    # ---------------------------------------------------
    root = Tk()
    root.attributes('-topmost', True)
    root.title('BIUI')
    #---------------------------------------------------
    bank_label = Label(root, text = "Bank")
    symbol_label = Label(root, text = "Symbol")
    price_label = Label(root, text = "Price")
    stop_label = Label(root, text = "Stop")
    limit_label = Label(root, text = "Limit")
    quantity_label = Label(root, text = "Quantity")
    sell_price_label = Label(root, text = "Sell price")
    bnb_balance_label = Label(root, text = "BNB balance: ")
    bnb_balance = Label(root, text = "No data")
    deals_left_label = Label(root, text = "Deals left: ")
    deals_left = Label(root, text="No data")
    #---------------------------------------------------
    Bank = Entry(root, width = 25)
    Symbol = Entry(root, width = 25)
    Price = Entry(root, width = 25)
    Stop = Entry(root, width = 25)
    Limit = Entry(root, width = 25)
    Quantity = Entry(root, width = 25)
    Sell_price = Entry(root, width = 25)
    #---------------------------------------------------
    BuyButton = Button(root, text = "Buy", state = DISABLED, command = lambda:
    buystoploss(Symbol.get(), Price.get(), Stop.get(), Limit.get(), Quantity.get(), Price))
    UpgradeButton = Button(root, text = "Upgrade", state = DISABLED, command = lambda: upgrade(Symbol.get(), Stop.get(), Limit.get(), Quantity.get()))
    AutolimitButton = Button(root, text = "↓", command = lambda: autolimit(Stop.get(), Limit))
    AutoquantityButton = Button(root, text = "Set", command = lambda: autoquantity(Bank.get(), Price.get(), Quantity))
    AutostopButton = Button(root, text = "↑", command = lambda: autostop(Stop.get(), Stop))
    Autostop3xButton = Button(root, text = "↑↑", command = lambda: autostop3x(Stop.get(), Stop))
    Data = Button(root, text = "Data", command = lambda: getData(Symbol.get(), bnb_balance, deals_left, Bank.get()))

    BuyOcoButton = Button(root, text = "BuyOco", command = lambda:
    ocobuystoploss(Symbol.get(), Price.get(), Sell_price.get(), Stop.get(), Limit.get(), Quantity.get(), Price))
    UpgradeOcoButton = Button(root, text="UpgradeOco",
                              command=lambda: upgrade_oco(Symbol.get(),Sell_price.get(), Stop.get(), Limit.get(), Quantity.get()))
    #---------------------------------------------------
    bank_label.grid(row = 0, column = 0)
    Bank.grid(row = 0, column = 3)

    #---------------------------------------------------
    symbol_label.grid(row = 1,column = 0)
    Symbol.grid(row = 1,column = 3)
    Data.grid(row = 1, column = 4)
    #---------------------------------------------------
    price_label.grid(row = 2,column = 0)
    Price.grid(row = 2, column = 3)
    #---------------------------------------------------
    stop_label.grid(row = 4, column = 0)
    Stop.grid(row= 4, column= 3)
    AutostopButton.grid(row = 4, column = 4)
    Autostop3xButton.grid(row = 4, column = 5)
    #---------------------------------------------------
    limit_label.grid(row = 5, column = 0)
    Limit.grid(row= 5, column= 3)
    AutolimitButton.grid(row = 5, column = 4)
    #---------------------------------------------------
    quantity_label.grid(row = 6,column = 0)
    Quantity.grid(row = 6, column = 3)
    AutoquantityButton.grid(row = 6, column = 4)
    #---------------------------------------------------
    sell_price_label.grid(row = 7, column = 0)
    Sell_price.grid(row = 7, column = 3)
    #---------------------------------------------------
    BuyButton.grid(row=8,column=2)
    UpgradeButton.grid(row=8,column=3)
    # ---------------------------------------------------
    BuyOcoButton.grid(row=9,column=2)
    UpgradeOcoButton.grid(row=9,column=3)
    #---------------------------------------------------
    bnb_balance_label.grid(row = 10, column = 0)
    bnb_balance.grid(row=10, column = 1)
    # ---------------------------------------------------
    deals_left_label.grid(row = 11, column = 0)
    deals_left.grid(row=11, column=1)


    root.mainloop()

