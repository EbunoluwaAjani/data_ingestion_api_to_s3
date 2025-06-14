import os
import time
from datetime import datetime

import awswrangler as wr
import boto3
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()
aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")


# Initialize AWS session
session = boto3.Session(
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name="eu-west-1"
)


def fetch_data(url: str) -> dict:
    """Fetch data from API with retry mechanism."""
    retries = 3
    for attempt in range(retries):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"Fetched data successfully on attempt {attempt + 1}")
                return response.json()
            print(f"Error {response.status_code} on attempt {attempt + 1}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
        time.sleep(6) 
        print('done with stage 1')


def extract_data(API_URL: str) -> pd.DataFrame:
    """Extract API response into a DataFrame with timestamp."""
    data = fetch_data(API_URL)
    if data:
        df = pd.DataFrame(data)
        df["Timestamp"] = datetime.now()
        return df


def load_to_s3(df: pd.DataFrame, s3_path: str):
    """Write DataFrame to S3."""
    if df.empty:
        print("DataFrame is empty. Skipping S3 upload.")
        return

    ingestion_date = datetime.now().strftime("%Y-%m-%d")
    file_name = f"weatherapifile_{ingestion_date}.parquet"
    full_s3_path = f"{s3_path}/{file_name}"

    wr.s3.to_parquet(
        df=df,
        path=full_s3_path,
        boto3_session=session,
        dataset=True,
        mode="append"
    )
    print("Data successfully written to S3!")


def etl_weather_to_s3(api_url: str, s3_path: str):
    df = extract_data(api_url)
    load_to_s3(df, s3_path)
