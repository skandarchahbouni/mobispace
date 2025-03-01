import logging
from airflow.providers.postgres.hooks.postgres import PostgresHook
from ..common import load_last_timestamp, save_last_timestamp
import pandas as pd
from airflow.providers.postgres.hooks.postgres import PostgresHook


def fetch_gps_data(**kwargs):
    """Fetches only new GPS data from PostgreSQL."""
    gps = load_last_timestamp(key="gps")
    logging.info(f"gps: {gps}")
    postgres_hook = PostgresHook(postgres_conn_id="mobispace_db")
    conn = postgres_hook.get_conn()
    cursor = conn.cursor()

    if gps:
        cursor.execute("SELECT * FROM gps WHERE timestamp > %s;", (gps,))
    else:
        cursor.execute("SELECT * FROM gps;")  # Load all if no timestamp is found

    data = cursor.fetchall()
    cursor.close()
    conn.close()

    if data:
        kwargs["ti"].xcom_push(key="gps_data", value=data)


def preprocess_gps_data(**kwargs):
    """Function to preprocess GPS data using pandas."""
    ti = kwargs["ti"]
    raw_data = ti.xcom_pull(task_ids="read_gps_data", key="gps_data")

    if not raw_data:  # No new data
        return

    columns = ["participant_virtual_id", "timestamp", "latitude", "longitude"]
    df = pd.DataFrame(raw_data, columns=columns)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["timestamp"] = df["timestamp"].astype(str)

    ti.xcom_push(key="preprocessed_gps_data", value=df.to_dict(orient="records"))


def insert_gps_preprocessed_data(**kwargs):
    """Inserts preprocessed data into the gps_preprocessed table and updates last timestamp."""
    ti = kwargs["ti"]
    preprocessed_data = ti.xcom_pull(
        task_ids="preprocess_gps_data", key="preprocessed_gps_data"
    )

    if not preprocessed_data:  # No new data
        return

    postgres_hook = PostgresHook(postgres_conn_id="mobispace_db")
    conn = postgres_hook.get_conn()
    cursor = conn.cursor()

    latest_timestamp = None
    for record in preprocessed_data:
        participant_virtual_id, timestamp, latitude, longitude = (
            record["participant_virtual_id"],
            record["timestamp"],
            record["latitude"],
            record["longitude"],
        )
        insert_query = """
        INSERT INTO gps_preprocessed (participant_virtual_id, timestamp, lat, lon)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (participant_virtual_id, timestamp) DO NOTHING;
        """
        cursor.execute(
            insert_query, (participant_virtual_id, timestamp, latitude, longitude)
        )

        if latest_timestamp is None or timestamp > latest_timestamp:
            latest_timestamp = timestamp  # Keep track of the latest timestamp

    conn.commit()
    cursor.close()
    conn.close()

    if latest_timestamp:
        save_last_timestamp(latest_timestamp, key="gps")
