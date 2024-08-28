import datetime
import pandas_ta as ta
import pandas as pd
from backtesting import Backtest
from backtesting import Strategy
from backtesting.lib import crossover, barssince
from backtesting.test import GOOG


import datetime
import pandas_ta as ta
import pandas as pd
from backtesting import Backtest
from backtesting import Strategy
from backtesting.lib import crossover, barssince
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

        # If the daily RSI is above the upper bound and
        # 3 bars have passed since the RSI was last below the upper bound, close any open positions
        if self.daily_rsi[-1] > self.upper_bound and \
                barssince(self.daily_rsi < self.upper_bound) == 3:
            self.position.close()

        # If the daily RSI crosses below the lower bound, open a new buy position
        elif crossover(self.lower_bound, self.daily_rsi):
            self.buy()


# Set up the backtest with the Google stock data and the RSI strategy
bt = Backtest(GOOG, RsiOscillator, cash=10_000, commission=.002)

# Run the backtest and store the performance statistics
stats = bt.run()

# Print the trade history (all trades made during the backtest)
print(stats['_trades'].to_string())
