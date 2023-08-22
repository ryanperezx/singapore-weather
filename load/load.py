import requests
import logging
import json
import boto3    
import os

logger = logging.getLogger(__name__)
if logging.getLogger().hasHandlers():
    logging.getLogger().setLevel(logging.INFO)
else:
    logging.basicConfig(level=logging.INFO)



def lambda_handler(event: dict, context) -> requests.Response:
    s3_bucket_name = os.environ.get('BUCKET_NAME')
    dynamodb_table_name = os.environ.get('DYNAMODB_TABLE')
    s3_file_path = f'singapore_weather/{event["execution_datetime"]}.json'
    s3_client = boto3.client('s3')
    dynamodb_client = boto3.client('dynamodb')
    
    json_object = json.loads(s3_client.get_object(Bucket=s3_bucket_name, Key=s3_file_path))

    response = dynamodb_client.put_item(TableName=dynamodb_table_name, Item=json_object)

    return response