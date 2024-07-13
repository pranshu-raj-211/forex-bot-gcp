from pydantic import BaseModel
from abc import ABC, abstractmethod
from email_alerts import send_email


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
        self.open_trades = 0
        self.symbol = "EURUSD"

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
