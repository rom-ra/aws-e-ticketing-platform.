import json


def lambda_handler(event, context):
    """Steps 10-12: receive a booking request, save it, queue it."""
    print("booking-api received:", event)
    # Simple demo: pretend the seat was saved to DynamoDB and sent to SQS.
    body = {"message": "Booking received", "status": "PENDING", "seat": "A12"}
    return {"statusCode": 202, "body": json.dumps(body)}
