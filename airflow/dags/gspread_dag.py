from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from data_02 import processed_file

# Retrieve AWS credentials from Airflow Variables
aws_access_key = Variable.get("aws_access_key")
aws_secret_key = Variable.get("aws_secret_key")


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 6, 14),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'gspread_processing_dag',
    default_args=default_args,
    schedule_interval='@daily',
)


task = PythonOperator(
    task_id='run_gspread_script',
    python_callable=processed_file,  
    dag=dag,
)

task
