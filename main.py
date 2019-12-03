def pubFileMetaData(data, context):
    import json
    from google.cloud import pubsub_v1
    # project_id = "blaise-dev-258914"
    project_id = "blaisepoc"
    
    filename = data['name']

    ext = data['name'].split(".")[1].lower()
    if (ext == "csv") :
        topic_name = "uploadedFile"
        sourceName = "gcp_blaise_dde"
        dataset = "dde_blaise"
        iterationL1 = "\\\\ldata10"
        iterationL2 = ""
        iterationL3 = ""
        iterationL4 = ""
    elif ext == "asc" or ext == "rmk" or ext == "sps" :
        topic_name = "uploadedFile"
        sourceName = "gcp_blaise_dde"
        dataset = "dde_blaise"
        iterationL1 = "\\\\ldata12"
        iterationL2 = ""
        iterationL3 = ""
        iterationL4 = ""    

    client = pubsub_v1.PublisherClient()
    topic_path = client.topic_path(project_id, topic_name)

    version = context.event_id
    sizeBytes = data['size']
    md5hash = data['md5Hash']

    relativePath = ".\\"
    sensitivity = "High"
    manifestCreated = data['timeCreated']
    description = "GCP Blaise file trigger Manifest"
    schemaVersion = ""
    fullSizeMegabytes = data['size']/1000000

    msg = {}
    files = {}

    msg["version"] = f"{version}"
    files["sizeBytes"] = f"{sizeBytes}"
    files["name"] = f"{filename}"
    files["md5sum"] = f"{md5hash}"
    files["relativePath"] = f"{relativePath}"
    msg["files"] = f"[{files}]"
    msg["sensitivity"] = f"{sensitivity}"
    msg["sourceName"] = f"{sourceName}"
    msg["manifestCreated"] = f"{manifestCreated}"
    msg["description"] = f"{description}"
    msg["iterationL1"] = f"{iterationL1}"
    msg["iterationL2"] = f"{iterationL2}"
    msg["iterationL3"] = f"{iterationL3}"
    msg["iterationL4"] = f"{iterationL4}"
    msg["dataset"] = f"{dataset}"
    msg["schemaVersion"] = f"{schemaVersion}"
    msg["fullSizeMegabytes"] = f"{fullSizeMegabytes}"
    msgbytes = bytes(json.dumps(msg), encoding='utf-8')
    client.publish(topic_path, data=msgbytes)
