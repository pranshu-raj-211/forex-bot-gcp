from pydantic import BaseModel
from abc import ABC, abstractmethod


class StrategyValue(BaseModel):
    series: str
    stop_loss: float
    take_profit: float
    ma_period: int
    ma_type: str


class BaseStrategy:
    def __init__(self, value: StrategyValue) -> None:
        self.stop_loss = value.stop_loss
        self.take_profit = value.take_profit
        self.ma_type = value.ma_type
        self.ma_period = value.ma_period
        self.series = value.series

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

    @abstractmethod
    def enter(self, message: str):
        pass

    @abstractmethod
    def exit(self, message: str):
        pass
