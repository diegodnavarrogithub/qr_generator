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
    logger.info(f"S3 Bucket: {BUCKET}/{KEY}")
    s3 = boto3.client('s3')
    _id = event['queryStringParameters']['id']
    logger.info(f"Id: {_id}")
    now = datetime.now()

    try:
        response = s3.get_object(Bucket=BUCKET, Key=KEY)
        body_content = response['Body'].read()
        all_data = json.loads(body_content)
        # Logging info
        logger.info(f"All data: {json.dumps(all_data, indent=2)}")

        data = all_data.get(_id)
        if not data:
            return {
                'statusCode': 404,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Credentials": True
                    },
                'body': json.dumps('QR code not found')
            }
        url = data["URL"]

        # Update the LastAccessedAt timestamp
        data['LastAccessedAt'] = now.strftime("%Y-%m-%d")
        s3.put_object(Bucket=BUCKET, Key=KEY, Body=json.dumps(all_data))

        # Logging info
        logger.info(msg="Updated data: ", extra=json.dumps(all_data, indent=2))
        return {
            'statusCode': 302,
            'headers': {
                'Location': url,
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Credentials": True
            }
        }
    except Exception as e:
        logger.error(e)
        return {
            'statusCode': 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True
                },
            'body': json.dumps('Error occur')
        }
