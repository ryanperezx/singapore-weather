import requests
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def get_request_content(link, headers) -> str:
    request = requests.get(url=link, headers=headers)
    request.raise_for_status()
    request.close()
    return request.text


def extract(event, context):

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'
    }

    link = 'https://api.data.gov.sg/v1/environment/2-hour-weather-forecast'

    data = get_request_content(link, headers)

    logger.info(data)
    return 200