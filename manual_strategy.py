from tracemalloc import start
import yfinance as yf
import pandas as pd
import math
from datetime import date 

def run_strategy(symbol, sdate="2020-01-01", edate=date.today()):
    data = yf.download(symbol, sdate, edate)

    data["EMA5"] = data["Close"].rolling(5).mean()
    data["EMA7"] = data["Close"].rolling(7).mean()
    data["EMA150"] = data["Close"].rolling(150).mean()

    data["Buy_Signal"] = (data.EMA5 > data.EMA7).astype(int)
    data["Sell_Signal"] = ((data.EMA5 < data.EMA7) & (data.EMA5 < data.EMA150)).astype(int)

    start_cash = 10000
    cash = start_cash
    quantity = 0

    print("---", symbol, "---")
    for i in data.iterrows():
        close = i[1][3]
        ema5 = i[1][6]
        ema7 = i[1][7]
        ema150 = i[1][8]

        if (ema5 > ema7) and (cash != 0) and (not math.isnan(ema150)):
            quantity = cash / close
            print("---BUY---", " Date: ", i[0]," Cash: ", cash, " Close: ", close, " Quantity: ", quantity)
            cash = 0
        elif (ema5 < ema7) and (ema5 < ema150) and (quantity != 0):
            cash = quantity * close
            print("---SELL---", " Date: ", i[0], " Cash: ", cash, " Close: ", close)
            quantity = 0

    port_value = round(data.iloc[-1].Close * quantity, 2)
    pnl = port_value - start_cash
    perc_return = round(100 * pnl / start_cash, 2)

    return port_value, pnl, perc_return
    
    # data.to_csv("CHECKTHIS.csv")

