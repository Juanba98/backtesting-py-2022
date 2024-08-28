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

    # All initial calculations
    def init(self):
        # Convert the index of the Close price series to DatetimeIndex
        close_series = pd.Series(self.data.Close)
        close_series.index = pd.to_datetime(self.data.index)

        # Calculate the daily RSI using the specified window period
        self.daily_rsi = self.I(ta.rsi, close_series, self.rsi_window)

    def next(self):
        # If the daily RSI crosses above the upper bound
        if crossover(self.daily_rsi, self.upper_bound):
            if self.position.is_long:  # Check if there's an open long position
                self.position.close()  # Close the long position
                self.sell()  # Open a short position

        # If the daily RSI crosses below the lower bound
        elif crossover(self.lower_bound, self.daily_rsi):
            if self.position.is_short or not self.position:  # Check if there's an open short position or no position
                self.position.close()  # Close the short position (if any)
                self.buy()  # Open a long position


# Set up the backtest with the Google stock data and the RSI strategy
bt = Backtest(GOOG, RsiOscillator, cash=10_000, commission=.002)

# Run the backtest and store the performance statistics
stats = bt.run()

# Plot the backtest results
bt.plot(filename='RsiOscillator_reversal.html')
