import json
import logging
import os
from datetime import datetime

import boto3
from utils import generate_qr_code

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    data = json.loads(event["body"])
    destination_url = data.get("destination_url")
    if not destination_url:
        logger.error("No destination url was provided")
        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True,
            },
            "body": json.dumps({"error_message": "No destination url was provided"}),
        }

    if not destination_url.startswith("http"):
        logger.error("Destination url needs to start with http:// or https://")
        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True,
            },
            "body": json.dumps(
                {
                    "error_message": "Destination url needs to start with http:// or https://"
                }
            ),
        }

    logger.info(data)
    now = datetime.now()
    _id = now.strftime("%Y-%m-%d-%H:%M:%S.%f")
    domain_url = event.get("requestContext").get("domainName")
    stage = event.get("requestContext").get("stage")
    domain_url = f"https://{domain_url}/{stage}/redirect/{_id}"
    BUCKET = os.getenv("BUCKET_NAME")
    KEY = os.getenv("S3_KEY")
    s3 = boto3.client("s3")
    metadata = {
        "LastAccessedAt": now.strftime("%Y-%m-%d"),
        "URL": destination_url,
        "CreatedAt": now.strftime("%Y-%m-%d"),
    }
    logger.info(msg=f"New data for id ({_id}): {metadata}")
    status_code = 500
    try:
        response = s3.get_object(Bucket=BUCKET, Key=KEY)
        all_metadata = json.loads(response["Body"].read().decode("utf-8"))
        for cur_id, content in all_metadata.items():
            if destination_url == content.get("URL"):
                all_metadata[cur_id]["LastAccessedAt"] = now.strftime("%Y-%m-%d")
                break
        else:
            all_metadata[_id] = metadata

        s3.put_object(Bucket=BUCKET, Key=KEY, Body=json.dumps(all_metadata))
        status_code = 200

    except s3.exceptions.NoSuchKey as e:
        logger.error(e)
        s3.put_object(Bucket=BUCKET, Key=KEY, Body=json.dumps({_id: metadata}))

    return {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True,
        },
        "body": json.dumps(
            {
                "qr_image": (
                    generate_qr_code(domain_url)
                    if status_code == 200
                    else "Error generating qr code"
                )
            }
        ),
    }
