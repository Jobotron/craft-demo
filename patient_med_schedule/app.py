import json
import boto3
import uuid

_TableName = "PatientTable"
AttrName = "patientId"

client = boto3.client("dynamodb")

def lambda_handler(event, context):
    newId = uuid.uuid4()
    data = json.loads(event["body"])
    print(event)
    method = event["httpMethod"]
    if(method == "PUT"):
         patientId = event["pathParameters"]["Id"]
         resp = put_patient_schedule(patientId, data["name"], data["schedule"])
    elif (method == "POST"):
         resp = put_patient_schedule(str(newId), data["name"], data["schedule"])
    else:
        return {"statusCode": 405,
        "body":{}}
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