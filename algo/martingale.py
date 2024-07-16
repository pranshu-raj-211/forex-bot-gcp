import logging
from strategy import StrategyValue, BaseStrategy


class MartingaleStrategy(BaseStrategy):
    def __init__(self, value: StrategyValue, email_sender: callable) -> None:
        super().__init__(value, email_sender)
        self.position = 0
        self.entry_price = 0
        self.trade_count = 0

    def init_long(self):
        price = self.price_queue[-1]
        self.entry_price = price
        self.trade_count = 1
        self.position = 1
        self.enter(f'Entered the market at {price}')
        logging.info(f'Entered the market at {price}')

    def init_short(self):
        pass  # Implement if needed

    def go_long(self):
        price = self.price_queue[-1]
        if self.position == 0:
            self.init_long()
        elif self.position != 0 and price > self.entry_price:
            self.position = 0
            self.exit(f'Exited the market at {price}')
            logging.info(f'Exited the market at {price}')

    def go_short(self):
        pass  # Implement if needed

    def run(self, price: float):
        self.price_queue.append(price)
        self.go_long()