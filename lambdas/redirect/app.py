import json
import logging
import os
from datetime import datetime

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    BUCKET = os.getenv("BUCKET_NAME")
    KEY = os.getenv("S3_KEY")
    s3 = boto3.client('s3')
    _id = event['queryStringParameters']['id']
    logging.info(f"Id: {_id}")
    now = datetime.now()

    try:
        response = s3.get_object(Bucket=BUCKET, Key=KEY)
        all_data = json.loads(response['Body'])

        # Logging info
        logging.info(json.dumps(all_data, indent=2))


        data = all_data[_id]
        url = data["URL"]

        # Update the LastAccessedAt timestamp
        data['LastAccessedAt'] = now.strftime("%Y-%m-%d")
        s3.put_object(Bucket=BUCKET, Key=KEY, Body=json.dumps(all_data))

        # Logging info
        logging.info(json.dumps(all_data, indent=2))
        return {
            'statusCode': 302,
            'headers': {
                'Location': url,
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Credentials": True
            }
        }
    except Exception as e:
        return {
            'statusCode': 404,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True
                },
            'body': json.dumps('QR code not found')
        }
