import json
import boto3
import os
from sec_edgar import SecEdgar  # Import your SEC module

# Load SEC data from S3
S3_BUCKET = os.environ["S3_BUCKET"]
s3_client = boto3.client("s3")
SEC_DATA_KEY = "sec_data/latest_sec_data.json"  # Path in S3

def lambda_handler(event, context):
    request_type = event['request_type']
    company = event['company']
    year = event['year']
    
    try:
        # Load SEC data
        sec_data_obj = s3_client.get_object(Bucket=S3_BUCKET, Key=SEC_DATA_KEY)
        sec_data = json.loads(sec_data_obj["Body"].read())
        sec_lookup = SecEdgar(sec_data)

        # Find CIK
        cik = sec_lookup.name_to_cik(company) or sec_lookup.ticker_to_cik(company)
        if not cik:
            return {"statusCode": 400, "body": json.dumps("Invalid company name or ticker.")}

        if request_type == 'Annual':
            # Process annual request
            document = sec_lookup.annual_filing(cik, year)
        elif request_type == 'Quarter':
            quarter = event['quarter']
            # Process quarterly request
            document = sec_lookup.quarterly_filing(cik, year, quarter)
        else:
            return {"statusCode": 400, "body": json.dumps("Invalid request type. Use 'Annual' or 'Quarter'.")}

        return {
            'statusCode': 200,
            'body': json.dumps(document)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }
