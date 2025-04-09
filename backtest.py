import backtrader as bt
import pandas as pd

class MomentumStrategy(bt.Strategy):
    params = (
        ('lookback', 20),  # Period for momentum calculation
        ('hold_period', 5),
    )

    def __init__(self):
        self.sma = bt.indicators.SMA(self.data.close, period=self.p.lookback)
        self.order = None

    def next(self):
        if self.order:  # Skip if pending order
            return

        # Momentum logic: Buy if price > SMA, sell otherwise
        if self.data.close[0] > self.sma[0] and not self.position:
            size = self.broker.getvalue() * 0.9 / self.data.close[0]  # Use 90% of cash
            self.buy(size=size)
        elif self.data.close[0] < self.sma[0] and self.position:
            self.close()

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    
    # Load historical data (example: EUR/USD)
    data = bt.feeds.YahooFinanceData(
        dataname='EURUSD=X',
        fromdate=pd.to_datetime('2020-01-01'),
        todate=pd.to_datetime('2023-12-31')
    )
    cerebro.adddata(data)
    
    cerebro.addstrategy(MomentumStrategy)
    cerebro.broker.set_cash(100000)
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
    
    results = cerebro.run()
    strat = results[0]
    
    print(f"Final Portfolio Value: {cerebro.broker.getvalue():.2f}")
    print(f"Sharpe Ratio: {strat.analyzers.sharpe.get_analysis()['sharperatio']:.2f}")
    cerebro.plot()