import json


def lambda_handler(event, context):
    """Steps 16-17: the payment provider calls back, then we tell Step Functions the task is done."""
    print("payment-webhook received:", event)
    return {"statusCode": 200, "body": json.dumps({"message": "Payment confirmed"})}
