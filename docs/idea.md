# Requirements

This document outlines the specific requirements for each module of the trading alerts system.

## Functional Requirements
These are the things the system needs to do:

1. **Ingestion Module**
    - Connect to a websocket endpoint to receive real-time market data.
   - Process the incoming data to get OHLCV (Open, High, Low, Close, Volume) information.
   - Remove duplicate data points using Redis, based on the trading symbol and timestamp.
   - Publish the processed and deduplicated OHLCV data to a Kafka topic named price. The message will contain the OHLCV data, and the trading symbol will be used as the key.

2. **Kafka Pub/Sub**

Use two Kafka topics:
- price: For OHLCV data from the Ingestion Module.
- signals: For trading alerts from the Trading Module.
- 
All messages on these topics will be in JSON format.
The price topic will use the trading symbol as the message key.


3. **Trading Module**
    - Consume OHLCV data from the price Kafka topic.
    - Include a submodule to calculate technical indicators like SMA, EMA, and RSI from the price data. This will be a library of reusable classes.
    - Implement predefined trading strategies that use the calculated indicators and price data to decide when to generate trade signals.
    - When a trade signal is generated, it should contain the timestamp, trading symbol, action (buy or sell), the price, and the name of the strategy.
    - Publish the generated trade signals to the signals Kafka topic.


4. **Dashboard**
    - Visualize historical price data as candlestick charts.
    - Overlay technical indicators (like SMA and EMA) on the charts.
    - Show markers on the chart indicating when buy and sell trades occurred.
    - Get trade signal data from the signals Kafka topic and historical data from the Timeseries Database.
    - Include simple password-based authentication to access the dashboard.


5. **Notification Service**
    - Consume trade signals from the signals Kafka topic.
    - Allow users to subscribe to receive notifications for specific trading symbols (initially, this will be managed in memory).
    - When a trade signal is received, send a notification to all users subscribed to that trading symbol (for now, this will be simulated as sending an email).


6. **Timeseries Database**
    - Store OHLCV data, calculated indicator values, and generated trade signals.
    - Assume the use of InfluxDB for this purpose.



## Tradeoffs Considered
Here are some other design decisions where I considered different options:


### Trading Module Symbol Configuration: Static vs. Dynamic
I considered whether the trading module should have a fixed list of trading symbols to process or if this list should be configurable at runtime. While a fixed list is simpler to start with, a dynamic configuration would provide more flexibility to easily change the symbols being monitored without needing to redeploy the module. For the initial version, a static configuration might be sufficient.

### Indicator Topic: Separate vs. Embedded
I also thought about having a separate Kafka topic just for the calculated indicator values. This could be useful for other services that might want to use this data. However, it adds complexity. For now, it seems simpler to either include the necessary indicator values in the trade signal messages or have the dashboard and timeseries database retrieve this data as needed.
