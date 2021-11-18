import json
#import boto3
import uuid

# import requests
_TableName = "PatientTable"
AttrName = "patientId"

def lambda_handler(event, context):
    # add dynamodb integration
    newId = uuid.uuid4()
    
    resp = put_patient_schedule(str(newId), event["name"], event["schedule"]["daysOfWeek"], event["schedule"]["times"])
    return {
        "statusCode": 200,
        "body": json.dumps({"patientId":resp}),
    }

def put_patient_schedule(patientId, name, daysOfWeek, times):
     # get dynamodb client and perform operation
   #client = boto3.client("dynamodb")
  # client.put_item(
   return patientId