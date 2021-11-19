import json
import boto3
import uuid
from boto3.dynamodb.types import TypeDeserializer
_TableName = "PatientTable"
AttrName = "patientId"

client = boto3.client("dynamodb")

def lambda_handler(event, context):
    newId = uuid.uuid4()
    method = event["httpMethod"]
    if(method == "PUT"):
         patientId = event["pathParameters"]["Id"]
         data = json.loads(event["body"])
         resp = put_patient_schedule(patientId, data["name"], data["schedule"])
    elif(method =="GET"):
        patientId = event["pathParameters"]["Id"]
        resp = get_patient_schedule(patientId)
    elif (method == "POST"):
        data = json.loads(event["body"])
        resp = put_patient_schedule(str(newId), data["name"], data["schedule"])
    elif (method =="DELETE"):
        patientId = event["pathParameters"]["Id"]
        resp = delete_patient_schedule(patientId)
    else:
        return {"statusCode": 405,
        "body":{}}
    return {
        "statusCode": 200,
        "body": resp,
    }

def delete_patient_schedule(patientId):
    response = client.delete_item(
        TableName = _TableName,
        Key = {
            AttrName:{"S": patientId}
        }
    )
    print(response)
    return json.dumps({"patientId": patientId})

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

def get_patient_schedule(patientId):
    response = client.get_item(
        TableName = _TableName,
        Key = {
            "patientId":{"S": patientId}
        })

    # To go from low-level format to python
    deserializer = TypeDeserializer()
    name = deserializer.deserialize(response["Item"]['name'])
    sched = deserializer.deserialize(response["Item"]["schedule"])
    
    return json.dumps(
        {
            "patientId": patientId,
            "schedule": sched,
            "name":name
    }, default=set_default)

def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError