import datetime
import pandas_ta as ta
import pandas as pd
from backtesting import Backtest
from backtesting import Strategy
from backtesting.lib import crossover
from backtesting.test import GOOG


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

# Run the backtest and store the performance statistics
stats = bt.run()

# Plot the backtest results
bt.plot()
