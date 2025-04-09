from ib_insync import *
import pandas as pd

class LiveTradingBot:
    def __init__(self):
        self.ib = IB()
        self.ib.connect('127.0.0.1', 7497, clientId=1)  # TWS/Gateway
        
    def momentum_signal(self, symbol):
        bars = self.ib.reqHistoricalData(
            contract=Forex(symbol),
            endDateTime='',
            durationStr='20 D',
            barSizeSetting='1 day',
            whatToShow='MIDPOINT',
            useRTH=True
        )
        df = util.df(bars)
        sma = df['close'].rolling(20).mean().iloc[-1]
        last_close = df['close'].iloc[-1]
        return 'BUY' if last_close > sma else 'SELL'

    def place_order(self, symbol, action):
        contract = Forex(symbol)
        order = MarketOrder(action, 10000)  # Trade 10k units
        trade = self.ib.placeOrder(contract, order)
        print(f"Executed: {action} {symbol} at {trade.fills[0].execution.price}")

if __name__ == '__main__':
    bot = LiveTradingBot()
    signal = bot.momentum_signal('EURUSD')
    bot.place_order('EURUSD', signal)