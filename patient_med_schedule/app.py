import json
#import boto3
import uuid

# import requests
_TableName = "PatientTable"
AttrName = "patientId"

def lambda_handler(event, context):
    # add dynamodb integration
    newId = uuid.uuid4()
    data = json.loads(event["body"])
    
    resp = put_patient_schedule(str(newId), data["name"], data["schedule"])
    return {
        "statusCode": 200,
        "body": json.dumps({"patientId": resp}),
    }

def put_patient_schedule(patientId, name, schedule):
    print(schedule)
    return patientId