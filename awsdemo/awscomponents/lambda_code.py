import json

def lambda_handler(event, context):
    # Test code for te dynatrace demo test environment

    return {
        'statuscode': 200,
        'body': 'This response is from AWS Lambda function for Dynatrace demo environment'
    }