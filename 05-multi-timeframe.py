import datetime
import pandas_ta as ta
import pandas as pd
from backtesting import Backtest
from backtesting import Strategy
from backtesting.lib import crossover, resample_apply
from backtesting.test import GOOG


class RsiOscillator(Strategy):
    upper_bound = 70  # Upper RSI threshold, indicating overbought conditions
    lower_bound = 30  # Lower RSI threshold, indicating oversold conditions
    rsi_window = 14  # The period over which RSI is calculated

    # All initial calculations
    def init(self):
        # Ensure that the index is a DatetimeIndex for resampling
        close_series = pd.Series(self.data.Close)
        close_series.index = pd.to_datetime(self.data.index)

        # Calculate the daily RSI using the specified window period
        self.daily_rsi = self.I(ta.rsi, close_series, self.rsi_window)

        # Calculate the weekly RSI by resampling the data to weekly intervals (using Fridays as the end of the week)
        self.weekly_rsi = resample_apply(
            'W-FRI', ta.rsi, close_series, self.rsi_window)

    def next(self):
        # If the daily RSI crosses above the upper bound and the weekly RSI is also above the upper bound,
        # close any open positions (indicating overbought conditions on both daily and weekly RSI)
        if (crossover(self.daily_rsi, self.upper_bound) and
                self.weekly_rsi[-1] > self.upper_bound):
            self.position.close()

        # If the daily RSI crosses below the lower bound and the weekly RSI is below the lower bound,
        # open a new buy position (indicating oversold conditions on both daily and weekly RSI)
        elif (crossover(self.lower_bound, self.daily_rsi) and
                self.lower_bound > self.weekly_rsi[-1]):
            self.buy()


# Set up the backtest with the Google stock data and the RSI strategy
bt = Backtest(GOOG, RsiOscillator, cash=10_000, commission=.002)

# Run the backtest and store the performance statistics
stats = bt.run()

# Plot the backtest results
bt.plot(filename='RsiOscillator_multi_timeframe.html')
