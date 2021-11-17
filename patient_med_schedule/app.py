import json
#import boto3

# import requests


def lambda_handler(event, context):
    # add dynamodb integration
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "post",
            # "location": ip.text.replace("\n", "")
        }),
    }

#def put_patient_schedule(patientId, name, daysOfWeek, times):
     # get dynamodb client and perform operation

#    return response
