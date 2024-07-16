import json
import logging
import os
from datetime import datetime

import boto3


def lambda_handler(event, context):
    BUCKET = os.getenv("S3BUCKETDB")
    KEY = os.getenv("S3KEYDB")
    s3 = boto3.client('s3')
    _id = event['pathParameters']['id']
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
                'Location': url
            }
        }
    except Exception as e:
        return {
            'statusCode': 404,
            'body': json.dumps('QR code not found')
        }
