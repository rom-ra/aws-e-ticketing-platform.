"""Steps 10-12: POST /bookings. Hold the seat in DynamoDB, then queue the booking in SQS."""
import json
import os
import time

import boto3
from botocore.exceptions import ClientError

table = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])
sqs = boto3.client("sqs")
HOLD_SECONDS = int(os.environ.get("HOLD_SECONDS", "600"))


def respond(code, body):
    return {"statusCode": code, "headers": {"Content-Type": "application/json"}, "body": json.dumps(body)}


def lambda_handler(event, context):
    body = json.loads(event.get("body") or "{}")
    event_id, seat_id = body.get("eventId"), body.get("seatId")
    if not event_id or not seat_id:
        return respond(400, {"message": "eventId and seatId are required"})

    # The Cognito user comes from the JWT that API Gateway already checked
    claims = event["requestContext"]["authorizer"]["jwt"]["claims"]
    user_id, email = claims["sub"], claims.get("email", "")

    # Step 11: hold the seat. The condition stops two people booking the same seat.
    try:
        table.put_item(
            Item={"pk": event_id, "sk": seat_id, "status": "HELD", "userId": user_id,
                  "email": email, "expiresAt": int(time.time()) + HOLD_SECONDS},
            ConditionExpression="attribute_not_exists(pk) OR #s = :free",
            ExpressionAttributeNames={"#s": "status"},
            ExpressionAttributeValues={":free": "FREE"},
        )
    except ClientError as err:
        if err.response["Error"]["Code"] == "ConditionalCheckFailedException":
            return respond(409, {"message": "Seat is not available"})
        raise

    # Step 12: queue the booking so the workflow can run in the background
    sqs.send_message(
        QueueUrl=os.environ["QUEUE_URL"],
        MessageBody=json.dumps({"eventId": event_id, "seatId": seat_id, "userId": user_id, "email": email}),
    )
    return respond(202, {"message": "Booking received", "eventId": event_id, "seatId": seat_id, "status": "HELD"})
