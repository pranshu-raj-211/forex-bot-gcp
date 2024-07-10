"""Ingestion module for streaming price data"""

import logging
import os
import json
import random
import string
import re
from typing import Dict, Optional

from websocket import create_connection
from google.cloud import pubsub_v1


exitoninput = False
CREDENTIALS_PATH = (
    r"C:\Users\Pranshu\Desktop\forex-bot-gcp\trade-427812-26eefe90d0c1.json"
)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_PATH

publisher = pubsub_v1.PublisherClient()
TOPIC_PATH = "projects/trade-427812/topics/raw_data"


class IngestionPipe:
    """
    Creates an ingestor for the symbol and source uri specified.
    This uses a websocket connection to allow incoming streaming price data to be read by the system.
    """

    def __init__(
        self,
        symbol: str,
        output_file_path: str,
        uri: str,
        headers: Optional[Dict[str, str]],
    ) -> None:
        self.symbol = symbol
        self.uri = uri
        self.silent = True
        self.output = output_file_path
        self.exitoninput = False
        self.ws = None
        self.session = None
        self.chart_session = None
        self.stop_stream = False
        self.headers = headers
        self.logger = logging.getLogger("ingest")
        self.logger.propagate = False
        file_handler = logging.FileHandler("ingest.log")
        formatter = logging.Formatter("%(levelname)s - %(asctime)s - %(message)s")
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def generateSession(self):
        stringLength = 12
        letters = string.ascii_lowercase
        random_string = "".join(random.choice(letters) for i in range(stringLength))
        return "qs_" + random_string

    def generateChartSession(self):
        stringLength = 12
        letters = string.ascii_lowercase
        random_string = "".join(random.choice(letters) for i in range(stringLength))
        return "cs_" + random_string

    def prependHeader(self, st):
        return "~m~" + str(len(st)) + "~m~" + st

    def constructMessage(self, func, paramList):
        # json_mylist = json.dumps(mylist, separators=(',', ':'))
        return json.dumps({"m": func, "p": paramList}, separators=(",", ":"))

    def createMessage(self, func, paramList):
        return self.prependHeader(self.constructMessage(func, paramList))

    def sendRawMessage(self, ws, message):
        ws.send(self.prependHeader(message))

    def sendMessage(self, ws, func, args):
        ws.send(self.createMessage(func, args))

    def start_ws_connection(self):
        self.logger.warning("Starting new session")
        self.ws = create_connection(self.uri, skip_utf8_validation=True)
        self.session = self.generateSession()
        self.chart_session = self.generateChartSession()
        self.logger.warning("New session started")

        self.sendMessage(self.ws, "set_auth_token", ["unauthorized_user_token"])
        self.sendMessage(self.ws, "chart_create_session", [self.chart_session, ""])
        self.sendMessage(self.ws, "quote_create_session", [self.session])

        self.sendMessage(
            self.ws,
            "quote_set_fields",
            [
                self.session,
                "ch",
                "chp",
                "current_session",
                "description",
                "local_description",
                "language",
                "exchange",
                "fractional",
                "is_tradable",
                "lp",
                "lp_time",
                "minmov",
                "minmove2",
                "original_name",
                "pricescale",
                "pro_name",
                "short_name",
                "type",
                "update_mode",
                "volume",
                "currency_code",
                "rchp",
                "rtc",
            ],
        )
        self.sendMessage(
            self.ws,
            "quote_add_symbols",
            [self.session, self.symbol, {"flags": ["force_permission"]}],
        )
        self.sendMessage(self.ws, "quote_fast_symbols", [self.session, self.symbol])
        self.sendMessage(
            self.ws,
            "resolve_symbol",
            [
                self.chart_session,
                "symbol_1",
                '={"symbol":"'
                + self.symbol
                + '","adjustment":"splits","session":"extended"}',
            ],
        )
        if self.silent:
            self.sendMessage(
                self.ws,
                "create_series",
                [self.chart_session, "s1", "s1", "symbol_1", "1", 5000],
            )
        self.logger.warning("finished session setup")

    def message_filter(self, data):
        try:
            match = re.match(r"~m~(\d+)~m~(.*)", data)
            if match:
                length = int(match.group(1))
                message = json.loads(match.group(2).strip())
                if 80 <= length < 250 and message.get("m") != "critical_error":
                    return True
        except Exception:
            return False

    def run(self):
        """
        Run a persistent websocket connection, which runs for as long as no exceptions occur.
        """
        self.start_ws_connection()
        while True:
            try:
                if self.ws.connected:
                    result = self.ws.recv()
                    if not self.silent:
                        self.logger.info(result)
                    data = self.message_filter(result)
                    if data:
                        # todo: replace yield with kafka publish message
                        future = publisher.publish(
                            topic=TOPIC_PATH, data=result.encode("utf-8")
                        )
                        print(future.result())
                    else:
                        print(result)
                    if self.output and data:
                        with open(self.output, "a") as ww:
                            ww.write(result)
                            ww.write("\n")
                            ww.close()
                else:
                    self.logger.warning("Ws connection closed, retrying.")
                    self.start_ws_connection()
            except Exception as e:
                self.logger.exception("Unexpected exception occured", exc_info=True)

    def stop(self):
        self.stop_stream = True
        self.logger.warning("Stream stopping")


# if __name__ == "__main__":
#     headers = headers = json.dumps(
#         {
#             "Connection": "upgrade",
#             "Host": "data.tradingview.com",
#             "Origin": "https://data.tradingview.com",
#             "Cache-Control": "no-cache",
#             "Upgrade": "websocket",
#             "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits",
#             "Sec-WebSocket-Key": "2C08Ri6FwFQw2p4198F/TA==",
#             "Sec-WebSocket-Version": "13",
#             "User-Agent": "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.56",
#             "Pragma": "no-cache",
#         }
#     )

#     pipe = IngestionPipe(
#         symbol,
#         output,
#         uri,
#         headers=headers,
#     )
#     pipe.run()
