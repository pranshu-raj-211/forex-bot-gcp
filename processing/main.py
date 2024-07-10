import os
import logging

from google.cloud import pubsub_v1
from process import store_processed_data
from concurrent.futures import TimeoutError

logging.basicConfig(filename='raw_data_pull.log', format='%(level)s - %(asctime)s - %(message)s')

CREDENTIALS_PATH = r'C:\Users\Pranshu\Desktop\forex-bot-gcp\trade-427812-26eefe90d0c1.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = CREDENTIALS_PATH

raw_data_subscriber = pubsub_v1.SubscriberClient()
subscription_path = 'projects/trade-427812/subscriptions/raw_data-sub'

def callback(message):
    logging.debug(msg=message)
    print(message)
    raw_data = message.data.decode('utf-8')  # gets a string - message from ws (filtered to contain relevant info)
    store_processed_data(raw_data)
    message.ack()

streaming_pull_future = raw_data_subscriber.subscribe(subscription_path, callback=callback)

while True:
    with raw_data_subscriber:
        try:
            streaming_pull_future.result()
        except TimeoutError:
            streaming_pull_future.cancel()
            streaming_pull_future.result()