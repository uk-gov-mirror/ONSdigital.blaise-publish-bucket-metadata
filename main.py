import blaise_dds
from google.cloud import pubsub_v1

from models.config import Config
from models.message import File, Message

SUPPORTED_FILE_EXTENSIONS = [".zip"]

SUPPORTED_FILE_TYPES = ["dd", "mi"]


def size_in_megabytes(size_in_bytes):
    return "{:.6f}".format(int(size_in_bytes) / 1000000)


def create_message(event, config):
    file = File.from_event(event)

    msg = Message(
        sourceName=f"gcp_blaise_{config.env}",
        manifestCreated=event["timeCreated"],
        fullSizeMegabytes=size_in_megabytes(event["size"]),
        files=[file],
    )

    if file.extension() not in SUPPORTED_FILE_EXTENSIONS:
        print(
            f"File extension '{file.extension()}' is invalid, supported extensions: {SUPPORTED_FILE_EXTENSIONS}"
        )
        return None

    if file.type() not in SUPPORTED_FILE_TYPES:
        print(
            f"File type '{file.type()}' is invalid, supported extensions: {SUPPORTED_FILE_TYPES}"
        )
        return None

    if file.type() == "mi":
        return msg.management_information(config)
    if file.type() == "dd":
        return msg.data_delivery_opn(config, event)

    return None


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
