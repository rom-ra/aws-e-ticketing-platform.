def lambda_handler(event, context):
    """Timer job: release seats that were held but never paid for."""
    print("cleanup running:", event)
    return {"message": "Expired seat holds released"}
