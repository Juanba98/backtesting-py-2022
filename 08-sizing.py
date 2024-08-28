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
        # Calculate the daily RSI using the specified window period
        self.daily_rsi = self.I(ta.rsi, pd.Series(
            self.data.Close), self.rsi_window)

    def next(self):
        # Get the current price
        price = self.data.Close[-1]

        # If the daily RSI crosses above the upper bound, close any open positions
        if crossover(self.daily_rsi, self.upper_bound):
            self.position.close()

        # If the daily RSI is below the lower bound, open a new buy position
        elif self.lower_bound > self.daily_rsi[-1]:
            self.buy(size=1)  # Buy a fixed number of shares (1 share) if you don't have enough cash the operation doesn't triggered

            # Uncomment the line below to buy a percentage of the available cash instead of a fixed number of shares
            # self.buy(size=0.1)  # Buy with 10% of the available cash


# Set up the backtest with the Google stock data and the RSI strategy
bt = Backtest(GOOG, RsiOscillator, cash=100, commission=.002)

# Run the backtest and store the performance statistics
stats = bt.run()

# Plot the backtest results
bt.plot(filename='RsiOscillator_sizing.html')
