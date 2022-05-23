from datetime import datetime
import backtrader as bt


class DonchianChannels(bt.Indicator):
    alias = ('DCH', 'DonchianChannel',)

    lines = ('dcm', 'dch', 'dcl',)  
    params = dict(
        period=20,
        lookback=-1,  
    )

    plotinfo = dict(subplot=False) 
    plotlines = dict(
        dcm=dict(ls='--'), 
        dch=dict(_samecolor=True),  
        dcl=dict(_samecolor=True),  
    )

    def __init__(self):
        hi, lo = self.data.high, self.data.low
        if self.p.lookback:  
            hi, lo = hi(self.p.lookback), lo(self.p.lookback)

        self.l.dch = bt.ind.Highest(hi, period=self.p.period)
        self.l.dcl = bt.ind.Lowest(lo, period=self.p.period)
        self.l.dcm = (self.l.dch + self.l.dcl) / 2.0  

class MyStrategy(bt.Strategy):
    def __init__(self):
        self.myind = DonchianChannels()

    def next(self):
        if self.data[0] > self.myind.dch[0]:
            self.buy()
        elif self.data[0] < self.myind.dcl[0]:
            self.sell()

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(MyStrategy)
    cerebro.broker.setcash(100000.0)
    cerebro.broker.setcommission(commission=0.001)

    data = bt.feeds.YahooFinanceData(dataname='AAPL',
                                     fromdate=datetime(2020, 1, 1),
                                     todate=datetime(2022, 5, 22))
    cerebro.adddata(data)
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    beginning = cerebro.broker.getvalue()
    cerebro.run()
    print('Ending Portfolio Value: %.2f' % cerebro.broker.getvalue())
    ending = cerebro.broker.getvalue()
    cerebro.plot()
    
def advice():
    if beginning > ending:
      print("Stop trading. It's a harsh time for your stock.")
    elif:
      print("Just carry on. It's your fortune.")