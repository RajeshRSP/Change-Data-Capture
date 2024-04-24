# Change Data Capture using Replication Slot in Postgresql
## Overview:
This project aims to provide real-time tracking and analysis of changes happening in a PostgreSQL table. It employs a pipeline consisting of PostgreSQL, Kafka Connect, Apache Kafka, Apache Spark, and Streamlit to capture, process, and visualize database changes efficiently.

The main components of the project include:

- PostgreSQL Replication Slot: A replication slot is created in PostgreSQL to capture changes happening in the database tables.

- Kafka Connect: Configured to run a query at regular intervals, Kafka Connect reads data from the PostgreSQL replication slot and streams it to a Kafka topic.

- Apache Kafka: Acts as the central message broker, facilitating real-time data streaming between components.

- Apache Spark: Consumes the data stream from the Kafka topic, performs necessary transformations (using regular expressions), and processes the data to extract meaningful insights.

- Streamlit UI: A user-friendly interface built with Streamlit, allowing users to interactively query and visualize the processed data. Users can specify a date range to view table operations table-wise.

This pipeline enables users to monitor database changes in real-time, gain insights into data trends, and react promptly to critical events.


### Getting Started :

- Setting up a replication slot in postgresql:

    change these configurations in postgres:

        wal_level = logical
        max_replication_slots = 5
        max_wal_senders = 10

- Creation of replication slot:

         SELECT pg_create_logical_replication_slot('<slot_name>', '<decoding_plugin>');

- Verify creation of slot using:

        SELECT * FROM pg_replication_slots();

- Install Kafka :
      https://hevodata.com/blog/how-to-install-kafka-on-ubuntu/

- Setup Kafka Connect
    - Check <kakfa_installation_path>/libs to see if it has postgres.jar file and check whether that version is compatible with your psql version.
    - Create a folder /opt/kafka/connect and download confluentinc-kafka-connect-jdbc connector into this folder
    - Edit kafka/config/standalone properties.sh and change plugin path to the path where kafka connect is

    - Create kafka/config/jdbc-properties file and fill this :

            name=fulfillment-connector
            connector.class=io.confluent.connect.jdbc.JdbcSourceConnector
            tasks.max=1
            connection.url=jdbc:postgresql://<host>:<port>/<db>
            connection.user=<postgres user>
            connection.password=<postgres password>
            mode=bulk
            query=SELECT * FROM pg_logical_slot_get_changes('<replication_slot_name>', NULL, NULL)
            topic.prefix=<kafa_topic_name>
            poll.interval.ms=<time_interval>(in milliseconds)


- Run zookeeper:

        ./bin/zookeeper-server-start.sh config/zookeeper.properties

- Run Kafka:

        ./bin/kafka-server-start.sh config/server.properties



- Run Kafka connect:

        bin/connect-standalone.sh config/connect-standalone.properties config/jdbc-connector.properties


    Now our sql replication slot will be read by Kafka connect and the changes will be streamed to the Kafka topic that we specified


- Install Spark and run the code attached to: 
  - Read messages from the Kafka topic.
  - Extract information about table changes (inserts, updates, truncates, deletes) from the data .
  - Write the extracted information to Parquet files for easy storage and analysis.
- If required use streamlit to visualize the results for each table date wise by reading the data from parquet files


