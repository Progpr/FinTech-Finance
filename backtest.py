import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import backtrader as bt

def run_backtest(ticker, time, quantity):
    # Define the backtesting strategy parameters
    short_period = 50
    long_period = 200

    # Extract hourly data from Yahoo Finance for the specified time period
    if time == 10:
        start_date = '2014-1-1'
    elif time == 5:
        start_date = '2019-1-1'
    else:
        raise ValueError('Invalid time specified')
    end_date = '2024-1-1'
    data = yf.download(ticker, start=start_date, end=end_date, interval='1d')

    # Calculate moving averages
    data['short_sma'] = data['Close'].rolling(window=short_period).mean()
    data['long_sma'] = data['Close'].rolling(window=long_period).mean()
    data['crossover'] = data['short_sma'] - data['long_sma']

    # Backtesting strategy
    cerebro = bt.Cerebro()
    cerebro.adddata(bt.feeds.PandasData(dataname=data))

    class Strategy(bt.Strategy):
        params = (('short_period', short_period), ('long_period', long_period), ('trade_units', quantity))

        def __init__(self):
            self.first_trade = True
            self.short_sma = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.short_period)
            self.long_sma = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.long_period)
            self.crossover = bt.indicators.CrossOver(self.short_sma, self.long_sma)
            self.original_amount = None

        def next(self):
            if not self.position:
                if self.first_trade and self.crossover > 0:
                    self.buy(size=self.params.trade_units)
                    self.first_trade = False
                elif self.crossover > 0:
                    self.buy(size=self.params.trade_units)
            elif self.crossover < 0:
                self.sell(size=self.params.trade_units)

        def start(self):
            self.original_amount = self.params.trade_units * self.data.close[0]

        def stop(self):
            final_value = cerebro.broker.getvalue()
            return {'Original Amount Invested': self.original_amount, 'Final Value': final_value}

    cerebro.addstrategy(Strategy)
    cerebro.run()

    # Access the strategy instance directly
    strategy_instance = cerebro.run()[0]

    return strategy_instance.stop()
def generate_backtest_plot(ticker, time, quantity):
    # Extract hourly data from Yahoo Finance for the specified time period
    if time == 10:
        start_date = '2014-1-1'
    elif time == 5:
        start_date = '2019-1-1'
    else:
        raise ValueError('Invalid time specified')
    end_date = '2024-1-1'
    data = yf.download(ticker, start=start_date, end=end_date, interval='1d')

    # Define the backtesting strategy
    short_period = 50
    long_period = 200

    # Backtesting strategy
    cerebro = bt.Cerebro()
    cerebro.adddata(bt.feeds.PandasData(dataname=data))

    class Strategy(bt.Strategy):
        params = (('short_period', short_period), ('long_period', long_period), ('trade_units', quantity))

        def __init__(self):
            self.first_trade = True
            self.short_sma = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.short_period)
            self.long_sma = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.long_period)
            self.crossover = bt.indicators.CrossOver(self.short_sma, self.long_sma)

        def next(self):
            if not self.position:
                if self.first_trade and self.crossover > 0:
                    self.buy(size=self.params.trade_units)
                    self.first_trade = False
                elif self.crossover > 0:
                    self.buy(size=self.params.trade_units)
            elif self.crossover < 0:
                self.sell(size=self.params.trade_units)

        def start(self):
            self.original_amount = quantity * self.data.close[0]

        def stop(self):
            final_value = cerebro.broker.getvalue()
            return final_value
        
    cerebro.addstrategy(Strategy)
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trade_analyzer')
    cerebro.run()
    cerebro.plot(style='candlestick', volume=True)
    plt.savefig('backtest_plot.png')
    plt.close()
    return 'backtest_plot.png'

# Example usage:
ticker = "AAPL"
time = 10
quantity = 10

results = run_backtest(ticker, time, quantity)
print("Original Amount Invested:", results['Original Amount Invested'])
print("Final Value:", results['Final Value'])
