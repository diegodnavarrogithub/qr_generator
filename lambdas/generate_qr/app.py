import json
import logging
import os
from datetime import datetime

import boto3
from utils import generate_qr_code


def lambda_hanlder(event, context):
    data = json.loads(event['body'])
    destination_url = data['destination_url']
    now = datetime.now()
    domain_url = f"{data['domain_url']}/redirect/{now}"
    BUCKET = os.getenv("S3BUCKETDB")
    KEY = os.getenv("S3KEYDB")
    s3 = boto3.client('s3')
    _id = now.strftime("%Y-%m-%d-%H:%M:&S.%f")
    metadata = {
        'LastAccessedAt': now.strftime("%Y-%m-%d"),
        'URL': destination_url,
        'CreatedAt': now.strftime("%Y-%m-%d")
    }
    try:
        response = s3.get_object(Bucket=BUCKET, Key=KEY)
        all_metadata = json.loads(response['Body'].read().decode('utf-8'))
        all_metadata[_id] = metadata
        s3.put_object(Bucket=BUCKET, Key=KEY, Body=json.dumps(all_metadata))

    except s3.exceptions.NoSuchKey as e:
        logging.error(e)
        s3.put_object(Bucket=BUCKET, Key=KEY, Body=json.dumps({
            _id: metadata
        }))

    return {
        'statusCode': 200,
        'body': json.dumps({
            'qr_image': generate_qr_code(domain_url)
        })
    }
