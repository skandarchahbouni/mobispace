from ..common import load_last_timestamp, save_last_timestamp
from airflow.providers.postgres.hooks.postgres import PostgresHook
import pandas as pd
import logging


def fetch_measures_data(**kwargs):
    """Fetches only new measures data from PostgreSQL."""
    last_timestamp = load_last_timestamp(key="measures")
    logging.info(f"Last processed measures timestamp: {last_timestamp}")

    postgres_hook = PostgresHook(postgres_conn_id="mobispace_db")
    conn = postgres_hook.get_conn()
    cursor = conn.cursor()

    if last_timestamp:
        cursor.execute("SELECT * FROM measures WHERE time > %s;", (last_timestamp,))
    else:
        cursor.execute("SELECT * FROM measures;")

    data = cursor.fetchall()
    cursor.close()
    conn.close()

    if data:
        kwargs["ti"].xcom_push(key="measures_data", value=data)


def preprocess_measures_data(**kwargs):
    """Function to preprocess measures data using pandas."""
    ti = kwargs["ti"]
    raw_data = ti.xcom_pull(task_ids="read_measures_data", key="measures_data")

    if not raw_data:
        return

    columns = [
        "participant_virtual_id",
        "time",
        "PM2_5",
        "PM10",
        "PM1_0",
        "Temperature",
        "Humidity",
        "NO2",
        "BC",
        "activity",
        "event",
    ]
    df = pd.DataFrame(raw_data, columns=columns)
    df["time"] = pd.to_datetime(df["time"])
    df["time"] = df["time"].astype(str)

    ti.xcom_push(key="preprocessed_measures_data", value=df.to_dict(orient="records"))


def insert_measures_preprocessed_data(**kwargs):
    """Inserts preprocessed data into the measures_preprocessed table and updates the last timestamp."""
    ti = kwargs["ti"]
    preprocessed_data = ti.xcom_pull(
        task_ids="preprocess_measures_data", key="preprocessed_measures_data"
    )

    if not preprocessed_data:
        return

    postgres_hook = PostgresHook(postgres_conn_id="mobispace_db")
    conn = postgres_hook.get_conn()
    cursor = conn.cursor()

    latest_timestamp = None
    for record in preprocessed_data:
        insert_query = """
        INSERT INTO measures_preprocessed (
            participant_virtual_id, time, PM2_5, PM10, PM1_0, 
            Temperature, Humidity, NO2, BC, activity, event
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (participant_virtual_id, time) DO NOTHING;
        """
        cursor.execute(insert_query, tuple(record.values()))

        if latest_timestamp is None or record["time"] > latest_timestamp:
            latest_timestamp = record["time"]

    conn.commit()
    cursor.close()
    conn.close()

    if latest_timestamp:
        logging.info(f"Updating last timestamp for measures: {latest_timestamp}")
        save_last_timestamp(latest_timestamp, key="measures")
