from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from tasks.gps.main import (
    fetch_gps_data,
    insert_gps_preprocessed_data,
    preprocess_gps_data,
)

# Default arguments
default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 2, 9),
    "retries": 0,
}

# Define DAG
with DAG(
    dag_id="gps_preprocessing",
    default_args=default_args,
    schedule_interval=None,  # Run manually
    catchup=False,
) as dag:

    # Task 1: Read new GPS data
    read_gps_data = PythonOperator(
        task_id="read_gps_data",
        python_callable=fetch_gps_data,
    )

    # Task 2: Preprocess data
    preprocess_gps_data = PythonOperator(
        task_id="preprocess_gps_data",
        python_callable=preprocess_gps_data,
    )

    # Task 3: Create table if not exists
    create_gps_preprocessed_table = PostgresOperator(
        task_id="create_gps_preprocessed_table",
        postgres_conn_id="mobispace_db",
        sql=""" 
            CREATE TABLE IF NOT EXISTS gps_preprocessed (
                participant_virtual_id BIGINT NOT NULL,
                timestamp TIMESTAMP WITHOUT TIME ZONE NOT NULL,
                lat DECIMAL(10,7) NOT NULL,
                lon DECIMAL(10,7) NOT NULL,
                PRIMARY KEY (participant_virtual_id, timestamp)
            );
        """,
    )

    # Task 4: Insert processed data
    insert_gps_preprocessed_data = PythonOperator(
        task_id="insert_gps_preprocessed_data",
        python_callable=insert_gps_preprocessed_data,
    )

    # Define task dependencies
    (
        read_gps_data
        >> [preprocess_gps_data, create_gps_preprocessed_table]
        >> insert_gps_preprocessed_data
    )
