from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime


# Function to print Hello World
def hello_world():
    print("Hello, World!")


# Define the default_args for the DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2025, 2, 7),  # Set the start date
    "retries": 1,
}

# Define the DAG
dag = DAG(
    "hello_world_dag",
    default_args=default_args,
    description="A simple Hello World DAG",
    schedule_interval=None,  # Only run manually
)

# Define a task using PythonOperator
hello_task = PythonOperator(
    task_id="hello_world_task",
    python_callable=hello_world,
    dag=dag,
)

# Set the task sequence (although it's just one task)
hello_task
