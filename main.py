import json
import os

from google.cloud import pubsub_v1

from message import NiFiMessageProcessor


def publishMsg(data, context):
    project_id = os.getenv("PROJECT_ID")
    topic_name = os.getenv("TOPIC_NAME")
    env = os.getenv("ENV")
    on_prem_sub_folder = os.getenv("ON-PREM-SUBFOLDER")

    print(f"Configuration: Project ID: {project_id}")
    print(f"Configuration: Topic Name: {topic_name}")
    print(f"Configuration: File name: {data['name']}")
    print(f"Configuration: Bucket Name: {data['bucket']}")
    print(f"Configuration: ON-PREM-SUBFOLDER: {on_prem_sub_folder}")

    if project_id is None:
        print("project_id not set, publish failed")
        return

    nifi_msg_processor = NiFiMessageProcessor(env, on_prem_sub_folder)
    msg = nifi_msg_processor.create(data)
    print(f"Message {msg}")
    if msg is not None:
        client = pubsub_v1.PublisherClient()
        topic_path = client.topic_path(project_id, topic_name)
        msg_bytes = bytes(json.dumps(msg), encoding="utf-8")
        client.publish(topic_path, data=msg_bytes)
        print("Message published")
