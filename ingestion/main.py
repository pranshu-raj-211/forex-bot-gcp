import json
from ingest import IngestionPipe


headers = headers = json.dumps(
    {
        "Connection": "upgrade",
        "Host": "data.tradingview.com",
        "Origin": "https://data.tradingview.com",
        "Cache-Control": "no-cache",
        "Upgrade": "websocket",
        "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits",
        "Sec-WebSocket-Key": "2C08Ri6FwFQw2p4198F/TA==",
        "Sec-WebSocket-Version": "13",
        "User-Agent": "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.56",
        "Pragma": "no-cache",
    }
)

pipe = IngestionPipe(
    symbol="EURUSD",
    output_file_path="op.txt",
    uri="wss://data.tradingview.com/socket.io/websocket",
    headers=headers,
)

pipe.run()
