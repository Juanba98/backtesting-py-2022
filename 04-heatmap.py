import datetime
import pandas_ta as ta
import pandas as pd
from backtesting import Backtest
from backtesting import Strategy
from backtesting.lib import crossover, plot_heatmaps
from backtesting.test import GOOG
import matplotlib.pyplot as plt
import seaborn as sns
from pylab import savefig
import mpld3


def optim_func(series):
    if series['# Trades'] < 10:
        return -1
    else:
        return series['Equity Final [$]']/series['Exposure Time [%]']


class RsiOscillator(Strategy):
    upper_bound = 70
    lower_bound = 30
    rsi_window = 14

    # Do as much initial computation as possible
    def init(self):
        self.rsi = self.I(ta.rsi, pd.Series(self.data.Close), self.rsi_window)

    # Step through bars one by one
    # Note that multiple buys are a thing here

    def next(self):
        if crossover(self.rsi, self.upper_bound):
            self.position.close()
        elif crossover(self.lower_bound, self.rsi):
            self.buy()


bt = Backtest(GOOG, RsiOscillator, cash=10_000, commission=.002)
stats, heatmap = bt.optimize(
    upper_bound=range(55, 85, 5),
    lower_bound=range(10, 45, 5),
    rsi_window=range(10, 30, 2),
    maximize=optim_func,
    constraint=lambda param: param.upper_bound > param.lower_bound,
    return_heatmap=True,
)


# choose your colormaps from here
# https://matplotlib.org/stable/tutorials/colors/colormaps.html
hm = heatmap.groupby(["upper_bound", "lower_bound"]).mean().unstack()
svm = sns.heatmap(hm, cmap="plasma")
figure = svm.get_figure()
figure.savefig('svm_conf.png', dpi=400)


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

# Optimize the strategy parameters and return both stats and a heatmap
stats, heatmap = bt.optimize(
    upper_bound=range(55, 85, 5),  # Test upper RSI bounds from 55 to 80
    lower_bound=range(10, 45, 5),  # Test lower RSI bounds from 10 to 40
    rsi_window=range(10, 30, 2),  # Test RSI window periods from 10 to 28
    maximize=optim_func,  # Use the custom optimization function to maximize the strategy
    # Ensure upper bound is greater than lower bound
    constraint=lambda param: param.upper_bound > param.lower_bound,
    return_heatmap=True,  # Return a heatmap of the optimization results
)

# Process the heatmap data for visualization
hm = heatmap.groupby(["upper_bound", "lower_bound"]).mean().unstack()
# Create a heatmap using seaborn with the 'plasma' colormap
svm = sns.heatmap(hm, cmap="plasma")

# Save the heatmap figure as an HTML
plot_heatmaps(heatmap, agg='mean')


