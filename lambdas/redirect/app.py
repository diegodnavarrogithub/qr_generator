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
    _id = event['pathParameters']['qr_id']
    logger.info(f"Id: {_id}, type: {type(_id)}")
    now = datetime.now()

    try:
        response = s3.get_object(Bucket=BUCKET, Key=KEY)
        data_string = response['Body'].read().decode('utf-8')
        all_data = json.loads(data_string)
        logger.info(f"All data: {json.dumps(all_data, indent=2)}")

        data = all_data.get(_id)
        logger.info(f"Selected data: {data}")
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
        logger.info(f"URL: {url}")
        # Update the LastAccessedAt timestamp
        data['LastAccessedAt'] = now.strftime("%Y-%m-%d")
        logger.info(f"Updated selected data: {data}")
        s3.put_object(Bucket=BUCKET, Key=KEY, Body=json.dumps(all_data))
        # Logging info
        logger.info("Data saved")
        logger.info(msg=f"Updated data: {json.dumps(all_data, indent=2)}")
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
