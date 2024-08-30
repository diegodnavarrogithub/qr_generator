import json
import logging
import os
from datetime import datetime

import boto3
from utils import generate_qr_code

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    BUCKET = os.getenv("BUCKET_NAME")
    KEY = os.getenv("S3_KEY")
    logger.info(f"S3 Bucket: {BUCKET}/{KEY}")
    s3 = boto3.client('s3')
    now = datetime.now()
    to_be_deleted = []
    try:
        response = s3.get_object(Bucket=BUCKET, Key=KEY)
        data_string = response['Body'].read().decode('utf-8')
        all_data = json.loads(data_string)
        for _id, content in all_data.items():
            last_accessed = content.get("LastAccessedAt")
            last_accessed = datetime.strptime(last_accessed, "%Y-%m-%d")
            difference_in_days = (last_accessed - now).days
            if difference_in_days >= 90:
                to_be_deleted.append(_id)

        for _id in to_be_deleted:
            del all_data[_id]
        s3.put_object(Bucket=BUCKET, Key=KEY, Body=json.dumps(all_data))
    except Exception as e:
        logger.error(e)
