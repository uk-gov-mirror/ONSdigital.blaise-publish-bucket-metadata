import os
import base64
import binascii
import json
from google.cloud import pubsub_v1

def createMsg(data):

    msg = {
        "version": 3,
        "schemaVersion": 1,
        "files": [],
        "sensitivity": "High",
        "sourceName": "gcp_blaise_" + os.environ['ENV'],
        "description": "",
        "dataset": "",
        "iterationL1": "",
        "iterationL2": "",
        "iterationL3": "",
        "iterationL4": "",
        "manifestCreated": "",
        "fullSizeMegabytes": ""
    }

    files = {}
    filename = data['name'] + ":" + data['bucket']
    files["sizeBytes"] = data['size']
    files["name"] = filename
    decodehash = base64.b64decode(data['md5Hash'])
    encodehash = binascii.hexlify(decodehash)
    files["md5sum"] = str(encodehash, 'utf-8') # Note GCP uses md5hash - however, MiNiFi needs it to be md5sum
    files["relativePath"] = ".\\"
    msg['files'].append(files)
    fileExtn = data['name'].split(".")[1].lower()
    fileType = data['name'].split("_")[0].lower()

    runPubSub = False

    if fileExtn == "zip" and fileType == "mi":
        runPubSub = True
        msg["description"] = 'Management Information files uploaded to GCP bucket from Blaise5'
        msg["dataset"] = 'blaise_mi'
        msg["iterationL1"] = 'SurveyData'
        msg["iterationL2"] = os.getenv('ON-PREM-SUBFOLDER')
        msg["iterationL3"] = ''
        msg["iterationL4"] = ''
    elif fileExtn == "zip" and fileType == "dd":
        runPubSub = True
        msg["description"] = 'Data Delivery files uploaded to GCP bucket from Blaise5'
        msg["dataset"] = 'blaise_dde'
        msg["iterationL1"] = os.getenv('ON-PREM-SUBFOLDER')
        msg["iterationL2"] = data['name'][3:7].upper()
        msg["iterationL3"] = data['name'][7:8].upper()
        msg["iterationL4"] = ''
    else:
        runPubSub = False
        print("File extension {} not found or file type {} is invalid".format(fileExtn, fileType))

    if (runPubSub):
        msg["manifestCreated"] = data['timeCreated']
        msg["fullSizeMegabytes"] = "{:.6f}".format(int(data['size'])/1000000)
        return msg

def publishMsg(data, context):

    project_id = os.environ['PROJECT_ID']
    topic_name = os.environ['TOPIC_NAME']

    if(project_id):
        client = pubsub_v1.PublisherClient()
        topic_path = client.topic_path(project_id, topic_name)        
        msgbytes = bytes(json.dumps(createMsg(data)), encoding='utf-8')
        client.publish(topic_path, data=msgbytes)
