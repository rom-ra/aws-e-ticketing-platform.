"""Steps 16-17: POST /payments/webhook. The payment provider reports the result.
We update the seat and tell Step Functions to continue (or fail)."""
import json
import os

import boto3

table = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])
sfn = boto3.client("stepfunctions")


def respond(code, body):
    return {"statusCode": code, "body": json.dumps(body)}


def lambda_handler(event, context):
    body = json.loads(event.get("body") or "{}")  # {"eventId": "...", "seatId": "...", "paid": true}
    key = {"pk": body.get("eventId"), "sk": body.get("seatId")}
    item = table.get_item(Key=key).get("Item")
    if not item or "taskToken" not in item:
        return respond(404, {"message": "No payment is waiting for this seat"})

    if body.get("paid"):
        # Seat is sold: remove the hold timer so it never expires
        table.update_item(Key=key, UpdateExpression="SET #s = :b REMOVE expiresAt, taskToken",
                          ExpressionAttributeNames={"#s": "status"}, ExpressionAttributeValues={":b": "BOOKED"})
        sfn.send_task_success(taskToken=item["taskToken"], output="{}")
    else:
        sfn.send_task_failure(taskToken=item["taskToken"], error="PaymentDeclined", cause="Payment declined")
    return respond(200, {"message": "Payment result received"})
