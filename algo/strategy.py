from typing import Literal
from pydantic import BaseModel, validator, conint
from abc import ABC, abstractmethod
from email_alerts import send_email
from collections import deque


class StrategyValue(BaseModel):
    series: Literal[1, 2, 3, 4, 5]
    stop_loss: float
    take_profit: float
    ma_period: conint(gt=0)
    ma_type: str
    queue_max_length: conint(gt=0)

    @validator("queue_max_length")
    def check_queue_max_length_greater_than_ma_period(cls, v, values):
        if "ma_period" in values and v < values["ma_period"]:
            raise ValueError("queue_max_length cannot be less than ma_period")
        return v


class BaseStrategy:
    def __init__(self, value: StrategyValue) -> None:
        self.stop_loss = value.stop_loss
        self.take_profit = value.take_profit
        self.ma_type = value.ma_type
        self.ma_period = value.ma_period
        self.series = value.series
        self.open_trades = 0
        self.symbol = "EURUSD"
        self.queue = deque(maxlen=value.queue_max_length)

    @abstractmethod
    def init_long(self, queue):
        pass

    @abstractmethod
    def init_short(self, queue):
        pass

    @abstractmethod
    def go_long(self, queue):
        pass

    @abstractmethod
    def go_short(self, queue):
        pass

    def enter(self, message: str):
        send_email(message)

    @abstractmethod
    def exit(self, message: str):
        send_email(message)

    @abstractmethod
    def run(self):
        pass
