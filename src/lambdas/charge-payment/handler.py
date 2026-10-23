def lambda_handler(event, context):
    """Step 15: Step Functions asks the payment provider to charge the customer.
    The task token is kept so the payment-webhook can finish the task later."""
    print("charge-payment called with:", event)
    return {"message": "Charge requested from payment provider"}
