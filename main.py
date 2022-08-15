import pandas as pd
import numpy as np

import yfinance as yf

import matplotlib.pyplot as plt
import seaborn as sns

xle = pd.DataFrame(
    yf.Ticker("QQQ").history(period="4y")
)

xle["EMA5"] = xle["Close"].ewm(span=5).mean()
xle["EMA7"] = xle["Close"].ewm(span=7).mean()
xle["EMA150"] = xle["Close"].ewm(span=150).mean()

cols = ["Close", "EMA5", "EMA7", "EMA150"]

xle[cols].plot(kind="line")
plt.show()

xle["Signal"] = ((xle.Close < xle.EMA150) & (xle.EMA5 < xle.EMA7)).replace({True: "Hedge", False: "Cover"})

start_amount = 10000

for i in xle.iterrows():
    print(i["Signal"])
    break
