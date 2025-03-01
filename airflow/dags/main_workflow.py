from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.dummy_operator import DummyOperator
from tasks.gps.main import (
    fetch_gps_data,
    insert_gps_preprocessed_data,
    preprocess_gps_data,
)
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
    dag_id="main_workflow",
    default_args=default_args,
    schedule_interval=None,  # Run manually
    catchup=False,
) as dag:

    # Task 1: Read new GPS data
    read_gps_data = PythonOperator(
        task_id="read_gps_data",
        python_callable=fetch_gps_data,
    )

    # Task 2: Read new measures data
    read_measures_data = PythonOperator(
        task_id="read_measures_data",
        python_callable=fetch_measures_data,
    )

    # Task 3: Preprocess GPS data
    preprocess_gps_data = PythonOperator(
        task_id="preprocess_gps_data",
        python_callable=preprocess_gps_data,
    )

    # Task 4: Preprocess measures data
    preprocess_measures_data = PythonOperator(
        task_id="preprocess_measures_data",
        python_callable=preprocess_measures_data,
    )

    # Task 5: Create GPS preprocessed table if not exists
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

    # Task 6: Create measures preprocessed table if not exists
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

    # Task 7: Insert processed GPS data
    insert_gps_preprocessed_data = PythonOperator(
        task_id="insert_gps_preprocessed_data",
        python_callable=insert_gps_preprocessed_data,
    )

    # Task 8: Insert processed measures data
    insert_measures_preprocessed_data = PythonOperator(
        task_id="insert_measures_preprocessed_data",
        python_callable=insert_measures_preprocessed_data,
    )

    # Task 9: Stop classification & activities classification
    stop_detection = DummyOperator(task_id="stop_detection")
    activities_classification = DummyOperator(task_id="activities_classification")

    # Task 10: Saving the results
    saving_results = DummyOperator(task_id="saving_results")

    # Define task dependencies
    read_gps_data >> preprocess_gps_data
    read_measures_data >> preprocess_measures_data

    read_gps_data >> create_gps_preprocessed_table
    read_measures_data >> create_measures_preprocessed_table

    preprocess_gps_data >> insert_gps_preprocessed_data
    preprocess_measures_data >> insert_measures_preprocessed_data

    create_gps_preprocessed_table >> insert_gps_preprocessed_data
    create_measures_preprocessed_table >> insert_measures_preprocessed_data

    insert_gps_preprocessed_data >> stop_detection
    insert_measures_preprocessed_data >> stop_detection

    insert_gps_preprocessed_data >> activities_classification
    insert_measures_preprocessed_data >> activities_classification

    activities_classification >> saving_results
    stop_detection >> saving_results
