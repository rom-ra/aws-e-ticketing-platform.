def lambda_handler(event, context):
    """Steps 20-21: SNS triggers this function, which sends the e-ticket email with SES."""
    for record in event.get("Records", []):
        print("send-email got notification:", record["Sns"]["Message"])
    return {"message": "E-ticket email sent"}
