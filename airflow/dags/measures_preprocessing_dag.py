from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from tasks.measures.main import (
    fetch_measures_data,
    preprocess_measures_data,
    insert_measures_preprocessed_data,
)

# Default arguments
default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 2, 9),
    "retries": 0,
}

# Define DAG
with DAG(
    dag_id="measures_preprocessing",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
) as dag:

    # Task 1: Read new measures data
    read_measures_data = PythonOperator(
        task_id="read_measures_data",
        python_callable=fetch_measures_data,
    )

    # Task 2: Preprocess data
    preprocess_measures_data = PythonOperator(
        task_id="preprocess_measures_data",
        python_callable=preprocess_measures_data,
    )

    # Task 3: Create table if not exists
    create_measures_preprocessed_table = PostgresOperator(
        task_id="create_measures_preprocessed_table",
        postgres_conn_id="mobispace_db",
        sql=""" 
            CREATE TABLE IF NOT EXISTS measures_preprocessed (
                participant_virtual_id INT,
                time TIMESTAMP,
                PM2_5 INT,
                PM10 INT,
                PM1_0 INT,
                Temperature FLOAT,
                Humidity FLOAT,
                NO2 FLOAT,
                BC FLOAT,
                activity VARCHAR(255),
                event VARCHAR(255),
                PRIMARY KEY (participant_virtual_id, time)
            );
        """,
    )

    # Task 4: Insert processed data
    insert_measures_preprocessed_data = PythonOperator(
        task_id="insert_measures_preprocessed_data",
        python_callable=insert_measures_preprocessed_data,
    )

    # Define task dependencies
    (
        read_measures_data
        >> [preprocess_measures_data, create_measures_preprocessed_table]
        >> insert_measures_preprocessed_data
    )
