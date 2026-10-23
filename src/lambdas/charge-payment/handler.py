"""Step 15: called by Step Functions (State 2). Asks the payment provider to charge the customer.
The workflow then waits. We store its task token so the payment-webhook can resume it."""
import os

import boto3

table = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])


def lambda_handler(event, context):
    booking = event["booking"]
    table.update_item(
        Key={"pk": booking["eventId"], "sk": booking["seatId"]},
        UpdateExpression="SET taskToken = :t",
        ExpressionAttributeValues={":t": event["taskToken"]},
    )
    # A real system would call the payment provider here. This project only logs it.
    print("Charge requested for", booking["eventId"], booking["seatId"])
    return {"requested": True}
