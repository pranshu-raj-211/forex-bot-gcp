from collections import deque
import logging
from datetime import datetime

from strategy import BaseStrategy, StrategyValue

# todo : Replace messages in trading methods with message in enter function

# todo: Work out implementation of price and indicator queue, sharing


class PriceCrossover(BaseStrategy):
    """
    Implementation of a simple price crossover strategy.

    Currently exit conditions are not created, because it is difficult to track
    which signals are actually traded upon. Need to ensure this is
    implemented asap,, one way could be to have the dashboard have a trade button
    which redirects you to the particular trading platform.
    Trade button should have double tap for default website - fast action enabler.

    Entrypoint:
    - long: Price goes above moving average.
    - short: Price goes below moving average.

    Exit Conditions:
    - Profit or stop loss is hit.
    """

    # todo: implement an exit system, through id of trades (track each trade through stack)
    def __init__(self, value: StrategyValue) -> None:
        super().__init__(value)

    def init_long(self, queue, ma):
        condition = self.open_trades == 0 and queue[-1] > ma[-1] and queue[-2] <= ma[-2]
        if condition:
            time = datetime.now().strftime("%H:%M:%S")
            self.enter(direction='long', timestamp=time)

    def init_short(self, queue, ma):
        condition = self.open_trades == 0 and queue[-1] < ma[-1] and queue[-2] >= ma[-2]
        if condition:
            time = datetime.now().strftime("%H:%M:%S")
            self.enter(direction='short', timestamp=time)

    def go_long(self, queue, ma):
        condition = self.open_trades > 0 and queue[-1] > ma[-1] and queue[-2] <= ma[-2]
        if condition:
            time = datetime.now().strftime("%H:%M:%S")
            self.enter(direction='long', timestamp=time)

    def go_short(self, queue, ma):
        condition = self.open_trades > 0 and queue[-1] > ma[-1] and queue[-2] <= ma[-2]
        if condition:
            time = datetime.now().strftime("%H:%M:%S")
            self.enter(direction='short', timestamp=time)

    def run(self):
        return super().run()


value = StrategyValue(
    series=4,
    stop_loss=0.04,
    take_profit=0.08,
    ma_period=20,
    ma_type="sma",
    queue_max_length=20,
)
