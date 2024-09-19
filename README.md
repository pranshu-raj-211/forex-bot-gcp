# Forex-Bot-GCP

This project is a Python-based platform designed for algorithmic trading strategies on lower time frames (on the order of seconds). It provides a Pythonic interface to execute trades more efficiently than conventional trading platforms like TradingView or MetaTrader, which often have limitations on time frames. This bot does not currently integrate with brokers, but instead focuses on generating trading alerts and signals, helping traders find potential trade setups.

## Project Overview

The goal of this project is to facilitate the creation and execution of algorithmic trading strategies on very short time frames. It utilizes Google Cloud Pub/Sub to create an event-driven architecture that processes, publishes, and analyzes market data. Python is used to design the trading strategies, and real-time price data is ingested via websockets, primarily from TradingView.

I have limited the scope of this project to alerts creation and did not integrate any brokers, due to financial issues that come with algorithmic trading. Instead, this tool enables traders to find good trades based on some trading strategies and verify the trends, reducing the time they need to search for a good trading point.

### Tech stack used while starting the project

- Python as the programming language.
- Libraries - Websocket-client for data ingestion, Dash for dashboard.
- GCP for deployment of code and Pub/Sub.
- InfluxDB to store price and event data, which can be further used to improve the system.


Here's a brief, non comprehensive list of tasks that are done in this repo

- [x] Ingestion and filtering of messages from a data broker, used a websocket here to get data from TradingView's websocket.
- [x] Processing of the data received by the ingestor, to break it down into OHLCV data.
- [x] Publish the data using Pub/Sub, to enable downstream services to take advantage of it (Event Driven Architecture).
- [x] Creation of indicators, such as Moving averages, RSI, ATR to later use in trading strategies.
- [x] Using the indicators in a trading strategy and sending alerts when a signal (trade condition) occurs.
- [x] Sending emails to authorized traders when the trade condition occurs. 

Here's a list of the things that I have yet to do, but are in progress
- [ ] Testing of the push based Pub/Sub for the strategy module's function. This will enable it to be fully event driven and I can take advantage of lower timeframes better this way.
- [ ] Dashboard creation - Ongoing, made a simple dashboard for price and indicators using Plotly Dash, added an authentication layer but some things need to be fixed.
- [ ] Integration with InfluxDB to store data, to study patterns in data ingestion and processing later.

### Features I plan to add, contributions would be greatly appreciated

These features are mostly related to observability for now, I think that's the most lacking thing in this repo currently.
- [ ] End-toEnd tracing of messages throughout the project, from ingestion to other modules.
- [ ] Metrics related to the timing, frequency of data points and their type - Doable with a centralized logger.
- [ ] Integration with SNS to send messages instead of email (just seems more relevant to my users).
- [ ] Improve the websocket client to get messages of lower time frames still (sub second - bid ask spread).
- [ ] Refactor to new, faster websocket library, AWS services instead of GCP.


### Some changes since the start of this project

A couple of changes in the tech stack were made, notably the shift from GCP to AWS, owing to the fact that my account's access was restricted without explanation, therefore I'll need to migrate all of my services to AWS, which should be done by the end of October 2024.


Special thanks to [0xrushi](https://github.com/0xrushi), whose tradingview scraper was essential to my ingestion module, without it things would have been a lot more difficult and impractical to implement.
