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

def get_request_content(link, headers) -> requests.Response:
    request = requests.get(url=link, headers=headers)
    request.raise_for_status()
    request.close()
    return request


def lambda_handler(event: dict, context) -> requests.Response:

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'
    }
    if event is not None and event['execution_datetime']:
        link = f'https://api.data.gov.sg/v1/environment/2-hour-weather-forecast?date_time={event["execution_datetime"]}'
    else:
        link = 'https://api.data.gov.sg/v1/environment/2-hour-weather-forecast'

    s3_bucket = os.environ.get('BUCKET_NAME')

    data = get_request_content(link, headers)
    data = data.json()
    data['created_at'] = event['execution_datetime']

    s3 = boto3.client('s3')
    response = s3.put_object(
        Body=(bytes(data)),
        Bucket=s3_bucket,
        Key=f'singapore_weather/{event["execution_datetime"]}.json'
    )
    
    return response