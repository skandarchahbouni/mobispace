import threading
import psycopg2
import logging
import sys
import json
from confluent_kafka import Consumer, KafkaError

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# PostgreSQL Configuration
DB_CONFIG = {
    "dbname": "mobispace",
    "user": "admin",
    "password": "admin",
    "host": "database",
    "port": "5433",
}

# Kafka Consumer Configuration
KAFKA_CONF = {
    "bootstrap.servers": "kafka:9093",
    "group.id": "my_group",
    "auto.offset.reset": "earliest",
}


def insert_into_postgres(table, data):
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Replace empty strings with None (which will be translated to NULL in SQL)
        for key, value in data.items():
            if value == "":
                data[key] = None

        # Generate the SQL query dynamically based on table
        columns = ", ".join(data.keys())
        values = ", ".join(["%s"] * len(data))
        sql = f"INSERT INTO {table} ({columns}) VALUES ({values})"

        # Execute the insert query
        cursor.execute(sql, list(data.values()))
        conn.commit()

        logging.info(f"Inserted into {table}: {data}")

    except Exception as e:
        logging.error(f"Error inserting into {table}: {e}")
    finally:
        cursor.close()
        conn.close()


# Function to consume messages from a Kafka topic
def consume_topic(topic):
    consumer = Consumer(KAFKA_CONF)
    consumer.subscribe([topic])

    try:
        while True:
            msg = consumer.poll(5.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    logging.error(
                        f"[{topic} Consumer] End of partition {msg.partition()} {msg.offset()}"
                    )
                else:
                    logging.error(f"[{topic} Consumer] Error occurred: {msg.error()}")
            else:
                try:
                    message = json.loads(msg.value().decode("utf-8"))
                    logging.info(f"[{topic} Consumer] Consumed message: {message}")

                    # Insert into the correct table
                    insert_into_postgres(topic, message)

                except json.JSONDecodeError as e:
                    logging.error(
                        f"[{topic} Consumer] Failed to decode JSON message: {e}"
                    )
    finally:
        consumer.close()


# List of topics to consume
topics = ["gps", "measures"]

# Start a separate thread for each topic
threads = []
for topic in topics:
    thread = threading.Thread(target=consume_topic, args=(topic,))
    thread.start()
    threads.append(thread)

# Wait for all threads to complete
for thread in threads:
    thread.join()
