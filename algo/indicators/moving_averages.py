from abc import abstractmethod
from collections import deque


class MovingAverage():
    def __init__(self, ma_period: int) -> None:
        self.ma_period = ma_period
        # todo: set the max length later, this one is pretty arbitrary and not good for use
        self.indicator_queue = deque(maxlen=self.ma_period)
        self.value_sum = 0

    @abstractmethod
    def update(self, value, price_queue: deque):
        pass


    def get_most_recent_value(self):
        len_queue = len(self.indicator_queue)
        if len_queue == 0:
            return None
        # * Using len instead of negative indexing to reduce latency, see https://stackoverflow.com/questions/58526885/collections-deque-why-q9999-is-faster-than-q-1
        return self.indicator_queue[len_queue - 1]


class SimpleMovingAverage(MovingAverage):
    def __init__(self, ma_period: int) -> None:
        super().__init__(ma_period)

    def update(self, value, price_queue: deque):
        old_value = self.indicator_queue[0] if len(self.indicator_queue)>0 else 0
        self.indicator_queue.append(value)
        self.value_sum+=value
        if len(price_queue) >= self.ma_period:
            # implement moving average formula here
            self.value_sum-=old_value
            return self.value_sum/self.ma_period
        return None
        # otherwise do nothing?
