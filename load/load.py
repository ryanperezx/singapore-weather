import requests
import logging
import json
import boto3    
import os
import pytz
import datetime
from boto3.dynamodb.types import TypeSerializer

logger = logging.getLogger(__name__)
if logging.getLogger().hasHandlers():
    logging.getLogger().setLevel(logging.INFO)
else:
    logging.basicConfig(level=logging.INFO)

def serialize(json_object):
    serializer = TypeSerializer()
    serialized_item = serializer.serialize(vars(json_object) if hasattr(json_object, '__dict__') else json_object)

    return json_object if 'M' not in serialized_item else serialized_item['M']


def lambda_handler(event: dict, context) -> requests.Response:
    s3_bucket_name = os.environ.get('BUCKET_NAME')
    dynamodb_table_name = os.environ.get('DYNAMODB_TABLE')
    if event is not None and 'execution_datetime' in event.keys():
        s3_file_path = f'singapore_weather/{event["execution_datetime"]}.json'
    else:
        s3_file_path = datetime.now(pytz.timezone('Asia/Manila')).strftime('%Y-%m-%dT%H:%M:%S')
    
    s3_client = boto3.client('s3')
    dynamodb_client = boto3.client('dynamodb')
    
    json_object = json.loads(s3_client.get_object(Bucket=s3_bucket_name, Key=s3_file_path)['Body'].read())

    response = dynamodb_client.put_item(TableName=dynamodb_table_name, Item=json_object)

    return response