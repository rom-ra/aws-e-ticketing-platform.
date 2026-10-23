"""Steps 20-21: SNS delivers the TicketIssued event. Send the e-ticket email with SES."""
import json
import os

import boto3

ses = boto3.client("sesv2")


def lambda_handler(event, context):
    for record in event["Records"]:
        detail = json.loads(record["Sns"]["Message"])["detail"]  # EventBridge event sent through SNS
        ses.send_email(
            FromEmailAddress=os.environ["SENDER"],
            Destination={"ToAddresses": [detail["email"]]},
            Content={"Simple": {
                "Subject": {"Data": "Your e-ticket"},
                "Body": {"Text": {"Data": f"Your ticket for event {detail['eventId']}, seat {detail['seatId']} is confirmed."}},
            }},
        )
    return {"sent": len(event["Records"])}
