import base64
import binascii
import json
import os

import blaise_dds
from google.cloud import pubsub_v1


def createMsg(data):
    msg = {
        "version": 3,
        "schemaVersion": 1,
        "files": [],
        "sensitivity": "High",
        "sourceName": "gcp_blaise_" + os.environ["ENV"],
        "description": "",
        "dataset": "",
        "iterationL1": "",
        "iterationL2": "",
        "iterationL3": "",
        "iterationL4": "",
        "manifestCreated": "",
        "fullSizeMegabytes": "",
    }

    files = {}
    filename = data["name"] + ":" + data["bucket"]
    files["sizeBytes"] = data["size"]
    files["name"] = filename
    decodehash = base64.b64decode(data["md5Hash"])
    encodehash = binascii.hexlify(decodehash)
    files["md5sum"] = str(
        encodehash, "utf-8"
    )  # Note GCP uses md5hash - however, MiNiFi needs it to be md5sum
    files["relativePath"] = ".\\"
    msg["files"].append(files)
    fileExtn = data["name"].split(".")[1].lower()
    fileType = data["name"].split("_")[0].lower()

    runPubSub = False

    if fileExtn == "zip" and fileType == "mi":
        msg[
            "description"
        ] = "Management Information files uploaded to GCP bucket from Blaise5"
        msg["dataset"] = "blaise_mi"
        msg["iterationL1"] = os.getenv("ON-PREM-SUBFOLDER")
        msg["iterationL2"] = ""
        msg["iterationL3"] = ""
        msg["iterationL4"] = ""
    elif fileExtn == "zip" and fileType == "dd":
        msg["description"] = "Data Delivery files uploaded to GCP bucket from Blaise5"
        msg["dataset"] = "blaise_dde"
        msg["iterationL1"] = "SYSTEMS"
        msg["iterationL2"] = os.getenv("ON-PREM-SUBFOLDER")
        msg["iterationL3"] = data["name"][3:6].upper()
        msg["iterationL4"] = data["name"][3:11].upper()
    else:
        print(
            "File extension {} not found or file type {} is invalid".format(
                fileExtn, fileType
            )
        )
        return None

    msg["manifestCreated"] = data["timeCreated"]
    msg["fullSizeMegabytes"] = "{:.6f}".format(int(data["size"]) / 1000000)
    print(f"Message created {msg}")
    return msg


def publishMsg(data, context):
    project_id = os.getenv("PROJECT_ID", None)
    topic_name = os.getenv("TOPIC_NAME", None)
    dds_client = blaise_dds.Client(blaise_dds.Config.from_env())
    try:
        dds_client.update_state(data["name"], "in_nifi_bucket")

        print(f"Configuration: Project ID: {project_id}")
        print(f"Configuration: Topic Name: {topic_name}")
        print(f"Configuration: File name: {data['name']}")
        print(f"Configuration: Bucket Name: {data['bucket']}")
        print(
            f"Configuration: ON-PREM-SUBFOLDER: {os.getenv('ON-PREM-SUBFOLDER', None)}"
        )

        if project_id is None:
            print("project_id not set, publish failed")
            return

        msg = createMsg(data)
        print(f"Message {msg}")
        if msg is not None:
            client = pubsub_v1.PublisherClient()
            topic_path = client.topic_path(project_id, topic_name)
            msg_bytes = bytes(json.dumps(msg), encoding="utf-8")
            client.publish(topic_path, data=msg_bytes)
            print(f"Message published")
            dds_client.update_state(data["name"], "nifi_notified")

    except Exception as error:
        dds_client.update_state(data["name"], "errored", repr(error))
