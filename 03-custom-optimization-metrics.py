import datetime
import pandas_ta as ta
import pandas as pd
from backtesting import Backtest
from backtesting import Strategy
from backtesting.lib import crossover
from backtesting.test import GOOG

# Define a custom optimization function


def optim_func(series):
    # If there are fewer than 10 trades, return -1 (indicating a poor strategy)
    if series['# Trades'] < 10:
        return -1
    else:
        # Otherwise, maximize the ratio of final equity to exposure time
        return series['Equity Final [$]'] / series['Exposure Time [%]']

# Define a trading strategy class based on RSI (Relative Strength Index)


class RsiOscillator(Strategy):
    upper_bound = 70  # Upper RSI threshold, indicating overbought conditions
    lower_bound = 30  # Lower RSI threshold, indicating oversold conditions
    rsi_window = 14  # The period over which RSI is calculated

    def init(self):
        # Initialize the RSI indicator using the closing prices
        self.rsi = self.I(ta.rsi, pd.Series(self.data.Close), self.rsi_window)

    def next(self):
        # If RSI crosses above the upper bound, close any open position
        if crossover(self.rsi, self.upper_bound):
            self.position.close()
        # If RSI crosses below the lower bound, open a new buy position
        elif crossover(self.lower_bound, self.rsi):
            self.buy()


# Set up the backtest with the Google stock data and the RSI strategy
bt = Backtest(GOOG, RsiOscillator, cash=10_000, commission=.002)

# Optimize the strategy parameters using the custom optimization function
stats = bt.optimize(
    upper_bound=range(55, 85, 5),  # Test upper RSI bounds from 55 to 80
    lower_bound=range(10, 45, 5),  # Test lower RSI bounds from 10 to 40
    rsi_window=range(10, 30, 2),  # Test RSI window periods from 10 to 28
    maximize=optim_func,  # Use the custom optimization function to maximize the strategy
    # Ensure upper bound is greater than lower bound
    constraint=lambda param: param.upper_bound > param.lower_bound,
    # Uncomment the following line to use Random Grid search with a maximum of 100 tries
    # max_tries = 100
)

# Save the plot as an HTML file
bt.plot(filename='RsiOscillator_custom.html')
