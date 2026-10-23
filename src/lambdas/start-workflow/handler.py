"""Steps 13-14: read a booking from SQS and start the Step Functions workflow."""
import os

import boto3

sfn = boto3.client("stepfunctions")


def lambda_handler(event, context):
    for record in event["Records"]:
        sfn.start_execution(stateMachineArn=os.environ["STATE_MACHINE_ARN"], input=record["body"])
    return {"started": len(event["Records"])}
