# Architecture

The goal of this project is to create a trading alerts system that offers traders the flexibility to define their own strategies in code. This approach aims to speed up development, reduce costs, and provide a custom monitoring and evaluation setup.

## Module Breakdown and Design Considerations

Let's dive into each module of the system and discuss the design choices and tradeoffs I considered.

### 1. Ingestion

**Responsibility:** The Ingestion Module is the entry point for real-time market data. It connects to a websocket provided by a financial data broker, receives a continuous stream of market updates, and prepares this data for downstream processing.

**Technology Choice:** I chose Python for this module due to its its ease of use for data manipulation. Redis was selected for its fast in-memory key-value store capabilities, which are ideal for deduplication.

Note: Python websockets are incredibly inefficient. I will replace the websocket client with a more efficient one. An easy fix is to just implement your own websocket client with asyncio, but probably not worth it initially.


#### **Tradeoffs:**

* **Data Format Handling:** I'm assuming the websocket provides OHLCV data in JSON format for simplicity. However, in a real-world scenario, the data might come in various formats (e.g., raw ticks, order book updates). If that were the case, this module would need more complex parsing logic to aggregate the raw data into OHLCV candles. This would introduce additional complexity and potential performance considerations.
* **Websocket Connection Management:** Handling the connection to the websocket is crucial. I've considered implementing retries with exponential backoff to handle temporary disconnections. A tradeoff here is how many retries to attempt and what the maximum backoff time should be. Too few retries might lead to data loss, while too many could put unnecessary strain on the broker's server. Additionally, for persistent connection failures, the system might need to log alerts or even notify an operator.
* **Deduplication Strategy:** As discussed earlier, I opted for Redis with the `setex` command for deduplication. The key will be a combination of the trading symbol and the timestamp of the OHLCV data. The TTL of 60 seconds is chosen based on the assumption that duplicate messages are likely to arrive within a short timeframe. An alternative I considered was using Bloom filters. While more memory-efficient for very high data volumes, Bloom filters have a chance of false positives, which could lead to valid data points being discarded. For financial data, accuracy is paramount, so Redis's precise checking seemed more appropriate initially.

**Interaction with other modules:** The Ingestion Module will act as a publisher, sending the processed and deduplicated OHLCV data to a Kafka topic.

### 2. Kafka Pub/Sub

**Responsibility:** Kafka serves as the central message bus, enabling asynchronous communication and decoupling between different modules of the system. This allows each module to operate independently and scale as needed.

**Technology Choice:** Kafka is a popular choice for high-throughput, fault-tolerant messaging and is well-suited for real-time data streams like market data.

#### **Tradeoffs:**

* **Number of Topics:** I decided on two main topics initially: `price` for the OHLCV data and `signals` for the trading alerts. I considered whether more granular topics might be needed in the future (e.g., a separate topic for raw ticks if we decide to process them later). However, for simplicity, starting with these two core topics seems reasonable.
  
* **Message Serialization Format:** I chose JSON as the message format for its readability and ease of use. While more efficient binary formats like Avro or Protocol Buffers could offer better performance and schema evolution capabilities, JSON provides a good balance for this initial stage.

* **Partitioning Strategy:** For the `price` topic, I decided to use the trading symbol as the key. This ensures that all price updates for a specific symbol are routed to the same partition and processed in order by consumers within that partition. This is crucial for accurate indicator calculations. A potential issue here is data skew – if some symbols are traded much more frequently than others, the partitions for those symbols might become overloaded. Mitigation strategies could include increasing the number of partitions or potentially re-evaluating the partitioning key if skew becomes a significant problem.

**Interaction with other modules:** The Ingestion Module publishes to the `price` topic. The Trading Module, Dashboard, Notification Service, and Timeseries Database will subscribe to relevant topics.

### 3. Trading Module (with Indicators)

**Responsibility:** The Trading Module is responsible for implementing the core trading logic. It consumes the processed market data, calculates technical indicators, and applies predefined trading strategies to generate trade signals.

**Technology Choice:** Python was chosen for its rich ecosystem of libraries for data analysis and algorithmic trading.

#### **Tradeoffs:**

* **Indicator Implementation:** I decided to implement the technical indicators (SMA, EMA, RSI) as a library within the Trading Module. This keeps the indicator logic closely coupled with the trading strategies that use them. An alternative would be to create a separate microservice for indicator calculations. This could offer better isolation and potential for scaling the indicator calculation independently, but it would also introduce network latency and increased complexity. For this initial system, a library seems like a good balance.

* **Strategy Implementation:** I'm starting with hardcoded trading strategies directly within the Trading Module. This is simpler for initial development. However, for a more advanced system, it would be beneficial to externalize these strategies, perhaps by allowing them to be defined in configuration files or even through a dedicated strategy management interface (`Remote Code Execution`). A tradeoff here is the added complexity of managing external strategies versus the increased flexibility and agility they provide. Security would also be a major consideration if external strategies were allowed.

* **Data Storage for Indicators:** The indicator calculations will require historical price data. I'm assuming this will be managed within the indicator classes themselves, perhaps using queues to store a window of recent prices. For more complex strategies that require longer historical lookbacks or for backtesting purposes, a more robust solution might be needed, potentially involving querying the Timeseries Database.

**Interaction with other modules:** The Trading Module subscribes to the `price` topic to receive market data and publishes trade signals to the `signals` topic.

### 4. Dashboard

**Responsibility:** The Dashboard provides a visual interface for traders and engineers to monitor the system's performance, visualize market data, and see when trades occurred.

**Technology Choice:** Dash, a Python framework for building analytical web applications, was chosen for its ease of use and ability to create interactive visualizations.

#### **Tradeoffs:**

* **Data Fetching Strategy:** For simplicity in this initial design, I'm assuming the Dashboard can directly query the Timeseries Database for historical OHLCV and indicator data. It will also consume trade signals from the `signals` Kafka topic for real-time updates. In a more complex system with many users and high query loads, it might be beneficial to introduce an API service between the Dashboard and the Timeseries Database to handle data aggregation and caching, improving performance and reducing direct load on the database.

* **Authentication Method:** I've specified simple password-based authentication for this initial version. For a production system, more robust authentication and authorization mechanisms (like OAuth 2.0) would be necessary.

**Interaction with other modules:** The Dashboard subscribes to the `signals` topic and queries the Timeseries Database.

### 5. Notification Service

**Responsibility:** The Notification Service is responsible for alerting subscribed users whenever a new trade signal is generated.

**Technology Choice:** No choice so far.

**Tradeoffs:**

* **Subscription Management:** I've initially proposed an in-memory subscription mechanism for simplicity. For a real-world system with many users, a more robust and scalable subscription service would be required, potentially using a dedicated database or a service like Redis.
  
* **Notification Channels (Expanded):** For this initial design, I'm focusing on simulating email notifications. However, a production system might need to support multiple notification channels like SMS, push notifications, or integration with other communication platforms. Integrating with each of these channels would involve different APIs and complexities.

* **Handling Delivery Failures:** The Notification Service needs to handle potential failures in sending notifications (e.g., email server down, invalid phone number). Implementing retries with appropriate backoff strategies and logging failed notifications would be important for ensuring reliability. Retries can be pushed to a retry queue and those jobs can be later picked up by message workers.

**Interaction with other modules:** The Notification Service subscribes to the `signals` topic.

### 6. Timeseries Database

**Responsibility:** The Timeseries Database provides persistent storage for all relevant data, allowing for historical analysis, backtesting, and powering the Dashboard.

**Technology Choice:** I've assumed the use of InfluxDB, which is specifically designed for handling time-stamped data and offers efficient querying capabilities for time-based data. Redis has a time series data structure which can be used alternatively.

### **Tradeoffs:**

* **Database Selection:** Other Timeseries Databases like TimescaleDB (which is built on PostgreSQL) or Prometheus could also be considered. The choice often depends on factors like the expected data volume, query patterns, scalability requirements, and existing infrastructure.

* **Data Retention Policies:** Defining clear data retention policies will be important to manage storage costs and ensure compliance with any regulatory requirements.

**Interaction with other modules:** The Ingestion Module and Trading Module will write data to the Timeseries Database. The Dashboard will read data from it.