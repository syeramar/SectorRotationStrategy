import backtrader as bt
import yfinance as yf

from datetime import date
import numpy as np

def run_strategy(ticker, sdate='2017-01-01', edate=date.today()):
    class firstStrategy(bt.Strategy):
        def __init__(self):
            self.ema5 = bt.indicators.ExponentialMovingAverage(self.data.close, period=5)
            self.ema7 = bt.indicators.ExponentialMovingAverage(self.data.close, period=7)
            self.ema150 = bt.indicators.ExponentialMovingAverage(self.data.close, period=150)

            self.cash = 10000
            self.count = 0

        def log(self, txt, dt=None):
            ''' Logging function for this strategy'''
            dt = dt or self.datas[0].datetime.date(0)
            return '%s, %s' % (dt.isoformat(), txt)

        def next(self):
            if not self.position:
                if self.ema5 > self.ema7:
                    f.write("--------------------BUY--------------------")
                    f.write("\n")
                    f.write(self.log('Close, %.2f' % self.data.close[0]))
                    f.write("\n")
                    f.write("Cash Available to Buy: " + str(self.cash))
                    f.write("\n")
                    f.write("EMA5 " + str(np.array(self.ema5)[0]))
                    f.write("\n")
                    f.write("EMA7 " + str(np.array(self.ema7)[0]))
                    f.write("\n")
                    self.count += (self.cash / self.data.close[0])
                    f.write("Stock Count: " + str(self.count))
                    f.write("\n")
                    self.buy(size= self.count)
                    self.cash = 0
                    
            else:
                if self.ema5 < self.ema7 and self.ema5 < self.ema150:
                    self.sell(size=self.count)

                    f.write("--------------------SELL--------------------")
                    f.write("\n")
                    f.write(self.log('Close, %.2f' % self.data.close[0]))
                    f.write("\n")
                    f.write("EMA5: " + str(np.array(self.ema5)[0]))
                    f.write("\n")
                    f.write("EMA7: " + str(np.array(self.ema7)[0]))
                    f.write("\n")
                    f.write("EMA150: " + str(np.array(self.ema150)[0]))
                    f.write("\n")
                    f.write("Stock Count: " + str(self.count))
                    f.write("\n")
                    self.cash = self.count * self.data.close[0]
                    f.write("Cash Available after Sell: " + str(self.cash))
                    f.write("\n")
                    self.count = 0

    data = bt.feeds.PandasData(dataname=yf.download(ticker, sdate, edate, auto_adjust=True))
    startcash = 10000.0
    cerebro = bt.Cerebro()
    cerebro.addstrategy(firstStrategy)
    cerebro.broker.setcash(startcash)
    cerebro.adddata(data)

    with open("log.txt", 'r+') as f:
        f.truncate(0)
        cerebro.run()

        # Get final portfolio Value
        portvalue = round(cerebro.broker.getvalue(), 2)
        pnl = portvalue - startcash
        perc_return = round(100 * pnl / startcash, 2)

        # Print out the final result
        f.write("--------------------RESULT--------------------")
        f.write("\n")
        f.write('Final Portfolio Value: ${}'.format(portvalue))
        f.write("\n")
        f.write('P/L: ${}'.format(pnl))
        f.write("\n")
        f.write("% Return: ${}".format(perc_return))
        f.write("\n")

    return portvalue, pnl, perc_return

    
