"""Runs every 5 minutes. Frees seats that were held but never paid for."""
import os
import time

import boto3
from boto3.dynamodb.conditions import Attr

table = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])


def lambda_handler(event, context):
    expired = table.scan(FilterExpression=Attr("status").eq("HELD") & Attr("expiresAt").lt(int(time.time())))["Items"]
    for item in expired:
        table.update_item(Key={"pk": item["pk"], "sk": item["sk"]}, UpdateExpression="SET #s = :f REMOVE expiresAt, taskToken",
                          ExpressionAttributeNames={"#s": "status"}, ExpressionAttributeValues={":f": "FREE"})
    return {"released": len(expired)}
