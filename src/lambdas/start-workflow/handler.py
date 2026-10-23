def lambda_handler(event, context):
    """Steps 13-14: read a message from SQS and start the Step Functions workflow."""
    for record in event.get("Records", []):
        print("start-workflow got message:", record.get("body"))
    return {"message": "Workflow started"}
