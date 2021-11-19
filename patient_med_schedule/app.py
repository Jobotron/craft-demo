import json
import boto3
import uuid

# import requests
_TableName = "PatientTable"
AttrName = "patientId"

client = boto3.client("dynamodb")

def lambda_handler(event, context):
    # add dynamodb integration
    newId = uuid.uuid4()
    data = json.loads(event["body"])
    
    resp = put_patient_schedule(str(newId), data["name"], data["schedule"])
    return {
        "statusCode": 200,
        "body": resp,
    }

def put_patient_schedule(patientId, name, schedule):
    response = client.put_item(
        TableName=_TableName,
        Item={
            AttrName:{"S":patientId},
            'name': {"S": name},
            'schedule':{
                "M":{
                "daysOfWeek":{"S": schedule["daysOfWeek"]},
                "times":{"SS":schedule["times"]}
                }
            }
        },
        ReturnValues='ALL_OLD'
    )
    print(response)
    return json.dumps({"patientId": patientId})