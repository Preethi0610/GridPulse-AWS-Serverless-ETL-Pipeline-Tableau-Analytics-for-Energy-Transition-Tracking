# GridPulse — Extraction Layer
# Deployed as an AWS Lambda function (gridpulse-extract)
# Trigger: manual / EventBridge schedule
# Role: gridpulse-lambda-role (AWSLambdaBasicExecutionRole + S3 write access)
#
# Pulls the Our World in Data energy dataset and lands it untouched
# in the raw zone of the S3 data lake.

import json
import boto3
import urllib.request

s3 = boto3.client('s3')

BUCKET = 'gridpulse-preethi-ds'
SOURCE_URL = 'https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-data.csv'
DEST_KEY = 'raw/owid-energy-data.csv'


def lambda_handler(event, context):
    with urllib.request.urlopen(SOURCE_URL) as response:
        data = response.read()

    s3.put_object(Bucket=BUCKET, Key=DEST_KEY, Body=data)

    return {
        'statusCode': 200,
        'body': json.dumps(f'Uploaded {len(data)} bytes to s3://{BUCKET}/{DEST_KEY}')
    }
