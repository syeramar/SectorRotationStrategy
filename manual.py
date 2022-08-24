import yfinance as yf
import pandas as pd
import scipy 

ticker = "QQQ"

data = yf.download(ticker, "2019-01-01", "2022-08-22")


data["EMA5"] = data["Close"].rolling(5).mean()
data["EMA7"] = data["Close"].rolling(7).mean()
data["EMA150"] = data["Close"].rolling(150).mean()

data["Buy_Signal"] = (data.EMA5 > data.EMA7).astype(int)
data["Sell_Signal"] = ((data.EMA5 < data.EMA7) & (data.EMA5 < data.EMA150)).astype(int)

data.to_csv("CHECKTHIS.csv")

