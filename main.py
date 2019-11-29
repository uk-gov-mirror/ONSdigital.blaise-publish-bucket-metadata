def pubFileMetaData(data, context):
    from google.cloud import pubsub_v1
    project_id = "blaisepoc"
    topic_name = "jcTest"
    client = pubsub_v1.PublisherClient()
    topic_path = client.topic_path(project_id, topic_name)
    import json
    version = context.event_id
    sizeBytes = data['size']
    md5sum = "md5todo"
    filename = data['name']
    relativePath = ".\\"
    sensitivity = ""
    sourceName = context.event_type
    manifestCreated = data['timeCreated']
    description = "Testing creation of Blaise Manifest Example"
    iterationL1 = ""
    iterationL2 = ""
    iterationL3 = ""
    iterationL4 = ""
    dataset = ""
    schemaVersion = ""
    fullSizeMegabytes = ""

    data = {}
    files = {}

    data["version"] = f"{version}"
    files["sizeBytes"] = f"{sizeBytes}"
    files["name"] = f"{filename}"
    files["md5sum"] = f"{md5sum}"
    files["relativePath"] = f"{relativePath}"
    data["files"] = f"[{files}]"
    data["sensitivity"] = f"{sensitivity}"
    data["sourceName"] = f"{sourceName}"
    data["manifestCreated"] = f"{manifestCreated}"
    data["description"] = f"{description}"
    data["iterationL1"] = f"{iterationL1}"
    data["iterationL2"] = f"{iterationL2}"
    data["iterationL3"] = f"{iterationL3}"
    data["iterationL4"] = f"{iterationL4}"
    data["dataset"] = f"{dataset}"
    data["schemaVersion"] = f"{schemaVersion}"
    data["fullSizeMegabytes"] = f"{fullSizeMegabytes}"
    print(json.dumps(data, sort_keys=True, indent=3))
    msg = bytes(json.dumps(data), encoding='utf-8')
    # When you publish a message, the client returns a future.
    client.publish(topic_path, data=msg)
