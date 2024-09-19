# forex-bot-gcp

This project is essentially a trading platform, made for algorithmic trading strategies only. It executes trades on a lower time frame than conventional platforms (order of seconds), and provides a Pythonic way of doing things. Overall this was 

This project was made to enable me to create algorithmic trading strategies easily and execute them on lower time frames than allowed on trading platforms online (Tradingview, Metatrader). It uses Python to create the trading strategies, which are enabled by Pub/Sub (sending of price and other data to the correct services). 

I have limited the scope of this project to alerts creation and did not integrate any brokers, due to financial issues that come with algorithmic trading. Instead, this tool enables traders to find good trades based on some trading strategies and verify the trends, reducing the time they need to search for a good trading point.


Here's a brief, non comprehensive list of tasks that are done in this repo

- [ ] Ingestion and filtering of messages from a data broker, used a websocket here to get data from TradingView's websocket.
- [ ] Processing of the data received by the ingestor, to break it down into OHLCV data.
- [ ] Publish the data using Pub/Sub, to enable downstream services to take advantage of it (Event Driven Architecture).
- [ ] Creation of indicators, such as Moving averages, RSI, ATR to later use in trading strategies.
- [ ] Using the indicators in a trading strategy and sending alerts when a signal (trade condition) occurs.
- [ ] Sending emails to authorized traders when the trade condition occurs. 

Here's a list of the things that I have yet to do, but are in progress
- [ ] Testing of the push based Pub/Sub for the strategy module's function. This will enable it to be fully event driven and I can take advantage of lower timeframes better this way.
- [ ] Dashboard creation - Ongoing, made a simple dashboard for price and indicators using Plotly Dash, added an authentication layer but some things need to be fixed.
- [ ] Integration with InfluxDB to store data, to study patterns in data arrival later.

### Features I plan to add, contributions would be greatly appreciated

These features are mostly related to observability for now, I think that's the most lacking thing in this repo currently.
- [ ] Tracing of messages throughout the project, from ingestion to other modules.
- [ ] Metrics related to the timing, frequency of data points and their type - Doable with a centralized logger.
- [ ] Integration with SNS to send messages instead of email (just seems more relevant to my users).


Special thanks to [0xrushi](https://github.com/0xrushi), whose tradingview scraper was essential to my ingestion module, without it things would have been a lot more difficult and impractical to implement.
