from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from datetime import datetime, timedelta
from main import etl_weather_to_s3

# Retrieve AWS credentials from Airflow Variables
aws_access_key = Variable.get("aws_access_key")
aws_secret_key = Variable.get("aws_secret_key")

api_key = Variable.get("api_key")

API_URL = f"https://api.weatherbit.io/v2.0/current?lat=35.7796&lon=-78.6382&key={api_key}"
S3_BASE_PATH = "s3://weather-api-bucket-4a3adcb1"

default_args = {
    "owner": "airflow",
    "start_date": datetime(2025, 6, 13),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "daily_weather_api_pipeline",
    default_args=default_args,
    schedule_interval="@daily",
)

etl_task = PythonOperator(
    task_id="etl_weather_to_s3",
    python_callable=etl_weather_to_s3,
    op_kwargs={"api_url": API_URL, "s3_path": S3_BASE_PATH},
    dag=dag
)

etl_task
