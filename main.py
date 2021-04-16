import base64
import binascii

import blaise_dds
from google.cloud import pubsub_v1

from models.config import Config
from models.message import File, Message


def md5hash_to_md5sum(md5hash):
    decode_hash = base64.b64decode(md5hash)
    encoded_hash = binascii.hexlify(decode_hash)
    return str(encoded_hash, "utf-8")


def size_in_megabytes(size_in_bytes):
    return "{:.6f}".format(int(size_in_bytes) / 1000000)


def create_message(event, config):
    file = File(
        name=f"{event['name']}:{event['bucket']}",
        sizeBytes=event["size"],
        md5sum=md5hash_to_md5sum(event['md5Hash']),
        relativePath=".\\",
    )

    msg = Message(
        sourceName=f"gcp_blaise_{config.env}",
        description="",
        dataset="",
        manifestCreated=event["timeCreated"],
        fullSizeMegabytes=size_in_megabytes(event["size"]),
        files=[file],
    )

    fileExtn = event["name"].split(".")[1].lower()
    fileType = event["name"].split("_")[0].lower()

    if fileExtn == "zip" and fileType == "mi":
        msg.description = (
            "Management Information files uploaded to GCP bucket from Blaise5"
        )
        msg.dataset = "blaise_mi"
        msg.iterationL1 = config.on_prem_subfolder
    elif fileExtn == "zip" and fileType == "dd":
        msg.description = "Data Delivery files uploaded to GCP bucket from Blaise5"
        msg.dataset = "blaise_dde"
        msg.iterationL1 = "SYSTEMS"
        msg.iterationL2 = config.on_prem_subfolder
        msg.iterationL3 = event["name"][3:6].upper()
        msg.iterationL4 = event["name"][3:11].upper()
    else:
        print(
            "File extension {} not found or file type {} is invalid".format(
                fileExtn, fileType
            )
        )
        return None

    print(f"Message created {msg}")
    return msg


def publishMsg(event, _context):
    config = Config.from_env()
    dds_client = blaise_dds.Client(blaise_dds.Config.from_env())
    try:
        dds_client.update_state(event["name"], "in_nifi_bucket")

        print(f"Configuration: Project ID: {config.project_id}")
        print(f"Configuration: Topic Name: {config.topic_name}")
        print(f"Configuration: File name: {event['name']}")
        print(f"Configuration: Bucket Name: {event['bucket']}")
        print(f"Configuration: ON-PREM-SUBFOLDER: {config.on_prem_subfolder}")

        if config.project_id is None:
            print("project_id not set, publish failed")
            return

        msg = create_message(event, config)
        print(f"Message {msg}")
        if msg is not None:
            client = pubsub_v1.PublisherClient()
            topic_path = client.topic_path(config.project_id, config.topic_name)
            msg_bytes = bytes(msg.json(), encoding="utf-8")
            client.publish(topic_path, data=msg_bytes)
            print(f"Message published")
            dds_client.update_state(event["name"], "nifi_notified")

    except Exception as error:
        dds_client.update_state(event["name"], "errored", repr(error))
