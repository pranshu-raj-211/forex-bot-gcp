import os
import logging

from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError

logger = logging.getLogger("output")
file_handler = logging.FileHandler("ohlcv.log")
format_process = logging.Formatter("%(levelname)s - %(asctime)s - %(message)s")
file_handler.setFormatter(format_process)
file_handler.setLevel(logging.DEBUG)
logger.propagate = False

CREDENTIALS_PATH = r'C:\Users\Pranshu\Desktop\forex-bot-gcp\trade-427812-26eefe90d0c1.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = CREDENTIALS_PATH
downstream_subscriber = pubsub_v1.SubscriberClient()
subscription_path = 'projects/trade-427812/subscriptions/show_ohlcv'

def callback(message):
    message_data = message.data.decode('utf-8')
    # message_data is a string, convert to list of numbers
    # ! Need to remove float in later versions, work entirely in int
    ohlcv = [float(number) for number in message_data.split(' ')]
    logger.debug(ohlcv)
    print(ohlcv)
    message.ack()

streaming_pull_future = downstream_subscriber.subscribe(subscription_path, callback=callback)

while True:
    with downstream_subscriber:
        try:
            streaming_pull_future.result()
        except TimeoutError:
            streaming_pull_future.cancel()
            streaming_pull_future.result()