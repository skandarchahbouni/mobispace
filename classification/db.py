import os
import psycopg2
import logging

logging.basicConfig(level=logging.INFO)


# Get PostgreSQL credentials from environment variables
user = os.getenv("POSTGRES_USER", "default_user")
password = os.getenv("POSTGRES_PASSWORD", "default_password")
host = os.getenv("POSTGRES_HOST", "localhost")
database = os.getenv("POSTGRES_DB", "default_db")


def connect_to_db():
    try:
        conn = psycopg2.connect(
            user=user, password=password, host=host, database=database
        )
        logging.info("Connected to PostgreSQL!")
        return conn
    except Exception as e:
        logging.error("Failed to connect to PostgreSQL:", str(e))
