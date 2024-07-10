"""Data processing module for streaming prices."""

import json
import re
import os
import logging

from google.cloud import pubsub_v1


FILE_PATH = "output3.txt"
logger = logging.getLogger(__name__)
# todo: instead of saving data to files, start working on sending it to other modules.

processing_handler = logging.FileHandler("processing.log")
format_process = logging.Formatter("%(levelname)s - %(asctime)s - %(message)s")
processing_handler.setFormatter(format_process)
processing_handler.setLevel(logging.WARNING)
logger.propagate = False

CREDENTIALS_PATH = (
    r"C:\Users\Pranshu\Desktop\forex-bot-gcp\trade-427812-26eefe90d0c1.json"
)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_PATH

publisher = pubsub_v1.PublisherClient()
PUBLISHER_PATH = "projects/trade-427812/topics/processed_data"


def get_ohlcv(data):
    """
    Extracts timestamp, open, high, low, close and volume from a filtered message.

    Args:
    - data: A string sample produced by the websocket input stream. This is filtered to include only those
    messages that contain price data, by observation of patterns of data created.

    Returns:
    - A list which contains the following info - [timestamp, open, high, low, close, volume].
    """
    data = re.match(r"~m~(\d+)~m~(.*)", data)
    if not data:
        logger.info("No match")
        return
    data = data.group(2).strip()
    try:
        data = json.loads(data)
        prices = (
            data.get("p", [None, {}])[1].get("s1", {}).get("s", [{}])[0].get("v", [])
        )
        if prices:
            return prices
    except json.decoder.JSONDecodeError:
        logger.exception("Unexpected json", exc_info=True)
    except Exception:
        logger.exception("Unexpected error while filtering", exc_info=True)
    return None


def store_processed_data(raw_data):
    """
    Function to oversee processing of obtained data."""
    # todo: refactor to reduce nesting, add error handling
    if raw_data:
        processed_data = get_ohlcv(raw_data)
        if processed_data:
            # create a space separated string instead of a list, does well with encoding
            # todo: after splitting the string convert each element back to float in downstream services, this is duplicated so create a separate util function.
            processed_str_data = " ".join(
                [str(value) for value in processed_data]
            ).strip()
            publisher.publish(
                topic=PUBLISHER_PATH, data=processed_str_data.encode("utf-8")
            )
        else:
            logger.error("Could not get ohlcv %s", raw_data, exc_info=True)
    else:
        logger.warning("End of stream")
