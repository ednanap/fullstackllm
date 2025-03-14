import json
import boto3
import requests
import os
from datetime import datetime

# AWS S3 Configuration
S3_BUCKET = os.environ["S3_BUCKET"] 
SEC_URL = "https://www.sec.gov/files/company_tickers.json"

def lambda_handler(event, context):
    try:
        headers = {'User-Agent': 'AWSLambdaSecProject/1.0 (enapoli1@example.com)'}
        response = requests.get(SEC_URL, headers=headers)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch SEC data. Status Code: {response.status_code}")

        data = response.json()
        file_name = f"sec_data_{datetime.utcnow().strftime('%Y-%m-%d')}.json"

        s3_client = boto3.client("s3")
        s3_client.put_object(
            Bucket=S3_BUCKET,
            Key=f"sec_data/{file_name}",
            Body=json.dumps(data),
            ContentType="application/json"
        )

        return {
            "statusCode": 200,
            "message": f"Successfully uploaded {file_name} to {S3_BUCKET}"
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "error": str(e)
        }
