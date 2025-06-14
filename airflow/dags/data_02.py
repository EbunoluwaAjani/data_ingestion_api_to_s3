import os

import awswrangler as wr
import boto3
import gspread
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

s3_path = "s3://google-sheet-bucket-4a3adcb1"



# Initialize AWS session
session = boto3.Session(
    aws_access_key_id= aws_access_key,
    aws_secret_access_key= aws_secret_key,
    region_name="eu-west-1"
)


def process_gspread_data():
    gc = gspread.service_account(filename='credentials.json')
    wks = gc.open("gspread_exe").sheet1
    data = wks.get_all_values()

    def clean_column_name(col_name):
        return col_name.strip().lower().replace(" ", "_")

    cleaned_headers = [clean_column_name(col) for col in data[0]]
    df = pd.DataFrame(data[1:], columns=cleaned_headers)
    return df

def load_to_s3(df: pd.DataFrame, s3_path: str):
    """Write DataFrame to S3."""
    if df.empty:
        print("DataFrame is empty. Skipping S3 upload.")
        return
    wr.s3.to_parquet(
        df=df,
        path=s3_path,
        boto3_session=session,
        dataset=True,
        mode="append"
    )
print("Data successfully written to S3!")

print("Data successfully written to S3!")

# Execute
def processed_file():
    df = process_gspread_data()
    load_to_s3(df, s3_path)

processed_file()



