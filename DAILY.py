import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import backtrader as bt

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(100000.0)
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

data = bt.feeds.YahooFinanceData(dataname='AAPL',
    fromdate=datetime(2020, 1, 1),
    todate=datetime(2022, 5, 22))

data = btfeeds.YahooFinanceCSVData(dataname='yahoo_finance_aapl.csv')

class PandasData(feed.DataBase):
    '''
    The ``dataname`` parameter inherited from ``feed.DataBase`` is the pandas
    DataFrame
    '''
    params = (
        ('datetime', None),
        ('open', -1),
        ('high', -1),
        ('low', -1),
        ('close', -1),
        ('volume', -1),
        ('openinterest', -1),
    )

class MyStrategy(bt.Strategy):
    def __init__(self):
        self.sma = btind.SimpleMovingAverage(period=15)

    def next(self):
        if self.sma > self.data.close:
            pass
        elif self.sma < self.data.close: 
            pass

def advice():
  if self.sma > self.data.close:
            indicator = "Bearish market incoming. Save your cash and trade slower."
            return indicator
        elif self.sma < self.data.close: 
            indicator = "Bullish market incoming. Be eager to buy stocks, but beware of trading races and suprising downturns."
            return indicator