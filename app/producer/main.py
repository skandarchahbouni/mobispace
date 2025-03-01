import time
import csv
import json
import logging
import sys
import threading
from confluent_kafka import Producer

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# Kafka Producer Configuration
conf = {"bootstrap.servers": "kafka:9093"}  # Adjust if needed
producer = Producer(conf)


def delivery_report(err, msg):
    if err is not None:
        logging.info(f"Message delivery failed: {err}")
    else:
        logging.info(f"Message delivered to {msg.topic()} [{msg.partition()}]")


# Function to read data from CSV and send to Kafka
def produce_from_csv(file_path, topic):
    try:
        with open(file_path, mode="r") as file:
            reader = csv.DictReader(file)  # Read CSV as dictionaries
            for row in reader:
                message = json.dumps(row)  # Convert row to JSON
                producer.produce(
                    topic, key="key", value=message, callback=delivery_report
                )
                producer.flush()  # Ensure message delivery
                if file_path == "./data/gps.csv":
                    time.sleep(0.1)
                else:
                    time.sleep(0.5)  # Adjust interval as needed
    except Exception as e:
        logging.error(f"Error reading CSV: {e}")
    finally:
        producer.flush()


if __name__ == "__main__":
    thread1 = threading.Thread(target=produce_from_csv, args=("./data/gps.csv", "gps"))
    thread2 = threading.Thread(
        target=produce_from_csv, args=("./data/measures.csv", "measures")
    )

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()
