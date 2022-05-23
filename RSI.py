from datetime import datetime
import backtrader as bt
import pandas as pd
import sqlalchemy
import setup_psql_environment
from models import Security, SecurityPrice

class Streak(bt.ind.PeriodN):
    lines = ('streak',)
    params = dict(period=2)  

    curstreak = 0

    def next(self):
        d0, d1 = self.data[0], self.data[-1]

        if d0 > d1:
            self.l.streak[0] = self.curstreak = max(1, self.curstreak + 1)
        elif d0 < d1:
            self.l.streak[0] = self.curstreak = min(-1, self.curstreak - 1)
        else:
            self.l.streak[0] = self.curstreak = 0

class ConnorsRSI(bt.Indicator):
    lines = ('crsi',)
    params = dict(prsi=3, pstreak=2, prank=100)

    def __init__(self):
        # Calculate the components
        rsi = bt.ind.RSI(self.data, period=self.p.prsi)
        streak = Streak(self.data)
        rsi_streak = bt.ind.RSI(streak.data, period=self.p.pstreak)
        prank = bt.ind.PercentRank(self.data, period=self.p.prank)

        # Apply the formula
        self.l.crsi = (rsi + rsi_streak + prank) / 3.0

class MyRSIStrategy(bt.Strategy):
    def __init__(self):
        self.myind = ConnorsRSI()

    def next(self):
        if self.myind.crsi[0] <= 10:
            self.buy()
        elif self.myind.crsi[0] >= 90:
            self.sell()

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(100000.0)
    cerebro.broker.setcommission(commission=0.001)

    db = setup_psql_environment.get_database()
    session = setup_psql_environment.get_session()

    query = session.query(SecurityPrice).join(Security). \
        filter(Security.ticker == 'AAPL'). \
        filter(SecurityPrice.date >= '2020-01-01'). \
        filter(SecurityPrice.date <= '2022-05-22').statement
    dataframe = pd.read_sql(query, db, index_col='date', parse_dates=['date'])
    dataframe = dataframe[['adj_open',
                           'adj_high',
                           'adj_low',
                           'adj_close',
                           'adj_volume']]
    dataframe.columns = columns = ['open', 'high', 'low', 'close', 'volume']
    dataframe['openinterest'] = 0
    dataframe.sort_index(inplace=True)

    data = bt.feeds.PandasData(dataname=dataframe)

    cerebro.adddata(data)
    cerebro.addstrategy(MyStrategy)
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